use std::{path::PathBuf};
use crate::lexer::{ltypes::{LineData, TypesObject}, self};

type WdDatas   = Vec<LineData>;
type ScopeData  = (TypesObject, WdDatas);

pub struct Widget<'a>{
  pub name      : String,
  pub master    : Box<[String]>,

  pub presets   : Box<[&'a Preset]>,
  
  pub atributs  : WdDatas,
  pub commands  : WdDatas,
}

pub struct WdVars{
  __master__ : String,
  pub others : WdDatas
}

pub struct Preset{
  pub name : String,
  pub others  : WdDatas
}

pub struct Method<'a>{
  pub name : String,
  pub parameters : Box<[String]>,

  pub widget : Widget<'a>

}

pub struct WdTemplate{
  pub name    : String,

  pub widgets : Vec<Widget<'static>>,
  pub wd_vars : WdVars,
  pub presets : Vec<Preset>,
  pub methods : Vec<Method<'static>>,

  pub script  : Option<PathBuf>
}

#[derive(Default)]
struct BoxScopes{
  main_scope : Option<ScopeData>,
  ld_global  : WdDatas,
  sub_scopes : Vec<ScopeData>,
  dest      : bool,
}

pub struct ScopesManager<'a>{
  pub comments : String,
  pub is_comment : bool,
  comment_count : i8,
  template : &'a mut WdTemplate,
  scopes : BoxScopes,
}

impl WdTemplate {

  pub fn new(file : &PathBuf, base_fnc : & PathBuf) -> Self{

    fn script_find(path : &PathBuf, name : &String) -> Option<PathBuf>{
      let script = path.join(format!("{name}.py"));
  
      if script.exists(){
        return Some(script);
      }
  
      return None;
    }

    let mut name  : String          = file.file_stem().unwrap().to_ascii_lowercase().to_str().unwrap().to_string();
    let script    : Option<PathBuf> = script_find(base_fnc, &name);

    if name == "__init__"{
      name = file.parent().unwrap().file_name().unwrap().to_ascii_lowercase().to_str().unwrap().to_string();
    }

    Self{
      name    : name.clone(),
      widgets : Vec::new(),
      wd_vars : WdVars { __master__: name, others: Vec::new() }, // add name
      presets : Vec::new(),
      methods : Vec::new(),
      script  : script
    
    }
  }

}

impl BoxScopes{
  fn get_dest<F>(& mut self, mut func : F)

  where
    F : FnMut(& mut ScopeData)
  {
    match self.dest{
      false => {func(& mut self.main_scope.as_mut().unwrap())},
      true => {func(& mut self.sub_scopes.last_mut().unwrap())}
    }

  }

}

impl<'a> ScopesManager<'a> {

  fn append_data(& mut self, linedata : lexer::ltypes::LineData){

    if self.comment_count == 0 {
      match linedata.kind{
        lexer::ltypes::TypesLineData::Local => {
          self.scopes.get_dest(|dest| {
            dest.1.push(linedata.clone());

          })
        },
        lexer::ltypes::TypesLineData::Global => {
          self.scopes.ld_global.push(linedata);

        },
      }

    }
    
  }

  fn pos_end(& mut self, kind : lexer::ltypes::TypesObject){
    match kind{
      lexer::ltypes::TypesObject::Sections(section_type) => {
        self.scopes.get_dest(|dest| {
          if section_type == lexer::ltypes::TypesSection::Comment{
            self.comment_count -= 1;

            if self.comment_count == 0{
              self.is_comment = false
            }
          }
          else if self.is_comment == false && kind == dest.0 {
            match section_type{
              lexer::ltypes::TypesSection::Widget   => {
                // self.template.create_element_widget()
              }
              lexer::ltypes::TypesSection::Wdvar    => {}
              lexer::ltypes::TypesSection::Preset   => {}
              lexer::ltypes::TypesSection::Comment  => {}
              lexer::ltypes::TypesSection::Method   => {}
            }
          }
        })
      },
      lexer::ltypes::TypesObject::Segments(_) => {
        self.scopes.dest = false
      }
    }
    
  }

  fn pos_start(& mut self, kind : lexer::ltypes::TypesObject){
    match kind{
      lexer::ltypes::TypesObject::Sections(section_type) => {
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
      lexer::ltypes::TypesObject::Segments(_) => {
        self.scopes.dest = true;
        self.scopes.sub_scopes.push((kind, WdDatas::new()))
      }
    }

  }

  fn create_object(& mut self, object : lexer::ltypes::Object){

    match object.postion{
      lexer::ltypes::Position::Start => {
        self.pos_start(object.kind)
      },
      
      lexer::ltypes::Position::End => {
        self.pos_end(object.kind)
      },

      lexer::ltypes::Position::Inline => {
        if self.comment_count == 0{
          self.comments = object.content.unwrap()
        }
      }
    }
  }

  pub fn from_token(& mut self, token : lexer::ltypes::Token) -> & Self{
    match token{
      lexer::ltypes::Token::Object(object) => {
        self.create_object(object);
      },

      lexer::ltypes::Token::LineData(ldata) => {
        self.append_data(ldata)
      },
    }

    return self;

  }
  
  pub fn new(templ : &'a mut WdTemplate) -> Self{
    return Self{
      comments : String::new(),
      comment_count : 0,
      template : templ,
      scopes : BoxScopes::default(),
      is_comment : false
    }

  }

}