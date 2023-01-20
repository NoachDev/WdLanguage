use crate::lexer::{ltypes::{LineData, TypesObject}, self};
use super::gtypes;

pub type WdDatas   = Vec<LineData>;
type ScopeData  = (TypesObject, WdDatas);

#[derive(Default)]
pub struct BoxScopes{
  pub main_scope  : Option<ScopeData>,
  pub comments    : Vec<String>,
  sub_scopes  : Vec<ScopeData>,
  dest        : bool,
}

pub struct ScopesManager<'a>{
  pub is_comment : bool,
  comment_count : i8,
  template : &'a mut gtypes::WdTemplate,
  scopes : BoxScopes,
}

impl BoxScopes{

  pub fn find_key(& mut self, find : &Vec<String>) -> Result<lexer::ltypes::LineData, String>{

    for (i, ld) in self.main_scope.as_ref().unwrap().1.iter().enumerate(){
      if find.contains(&ld.key){
        return Ok(self.main_scope.as_mut().unwrap().1.remove(i));
      }

    }

    return Err(format!("obrigatory one of this fields : {:?}", find));
  }

  pub fn get_segments(& mut self, segm : TypesObject) -> WdDatas{

    for (i, wd_ld) in self.sub_scopes.iter().enumerate(){
      if wd_ld.0 == segm{
        return self.sub_scopes.remove(i).1;

      }
    }

    return WdDatas::new();

  }

  fn get_dest(& mut self) -> & mut ScopeData{
    match self.dest{
      false => return self.main_scope.as_mut().unwrap(),
      true => return self.sub_scopes.last_mut().unwrap()
    }

  }

}

impl<'a> ScopesManager<'a> {
  fn create_elements(& mut self, section_types : lexer::ltypes::TypesSection, repo : & mut gtypes::Repository){
    match section_types{
      lexer::ltypes::TypesSection::Widget   => {
        self.template.create_element_widget(& mut self.scopes)
      }
      lexer::ltypes::TypesSection::Preset   => {
        repo.create_element_preset(& mut self.scopes)
      }
      lexer::ltypes::TypesSection::Method   => {
        self.template.create_element_method(& mut self.scopes)
        
      },
      _ => {}
    }

  }
  
  fn append_data(& mut self, mut linedata : lexer::ltypes::LineData, repo : & mut gtypes::Repository){
    
    if self.comment_count == 0 {
      match linedata.kind{
        lexer::ltypes::TypesLineData::Local => {
          let dest = self.scopes.get_dest();

          repo.put_vars(& mut linedata.value);

          if dest.0 == TypesObject::Sections(lexer::ltypes::TypesSection::Wdvar){
            repo.create_var(linedata)
          }
          
          else{
            dest.1.push(linedata)
          }

        },
        lexer::ltypes::TypesLineData::Global => {
          self.template.call_method(linedata)

        },
      }

    }
    
  }

  fn pos_end(& mut self, kind : TypesObject, repo : & mut gtypes::Repository){
    match kind{
      TypesObject::Sections(section_type) => {
        if section_type == lexer::ltypes::TypesSection::Comment{
          self.comment_count -= 1;

          if self.comment_count == 0{
            self.is_comment = false
          }
        }
        else if self.is_comment == false{
          self.create_elements(section_type, repo);
          self.scopes.sub_scopes.clear();
          self.scopes.comments.clear()
          
        }
      },
      TypesObject::Segments(_) => {
        self.scopes.dest = false
      }
    }

    
  }

  fn pos_start(& mut self, kind : TypesObject){
    match kind{
      TypesObject::Sections(section_type) => {
        if section_type == lexer::ltypes::TypesSection::Comment{
          self.comment_count += 1;
        }
        else if self.comment_count > 1{
          self.is_comment = true
        }
        else if self.is_comment == false{
          self.scopes.main_scope = Some((kind, WdDatas::new()))
        }

      }
      TypesObject::Segments(_) => {
        self.scopes.dest = true;
        self.scopes.sub_scopes.push((kind, WdDatas::new()))
      }
    }

  }

  fn create_object(& mut self, object : lexer::ltypes::Object, repo : & mut gtypes::Repository){

    match object.postion{
      lexer::ltypes::Position::Start => {
        self.pos_start(object.kind)
      },
      
      lexer::ltypes::Position::End => {
        self.pos_end(object.kind, repo)
      },

      lexer::ltypes::Position::Inline => {
        if self.comment_count == 0{
          self.append_comment(object.content.unwrap())
        }
      }
    }
  }

  pub fn append_comment(& mut self, text : String){
    self.scopes.comments.push(text)
  }

  pub fn from_token(& mut self, token : lexer::ltypes::Token, repo : & mut gtypes::Repository) -> & Self{
    match token{
      lexer::ltypes::Token::Object(object) => {
        self.create_object(object,repo);
      },

      lexer::ltypes::Token::LineData(ldata) => {
        self.append_data(ldata, repo)
      },
    }

    return self;

  }
  
  pub fn new(templ : &'a mut gtypes::WdTemplate) -> Self{
    return Self{
      comment_count : 0,
      template : templ,
      scopes : BoxScopes::default(),
      is_comment : false
    }

  }

}
