use pcre2::bytes::Captures;
use crate::lexer;

use super::{*, ltypes::DataValue};

pub fn create_object(capture : Captures, index : usize, class : &simbolys::SimbolysObjects, text : String ) -> Option<ltypes::Token>{
  
  let mut content : Option<String> = None;
  let mut pos : ltypes::Position;

  let simboly : String;

  let ind_chr : usize;


  if let Some(sbl) = capture.name("Start"){
    
    pos = ltypes::Position::Start ;
    
    ind_chr = sbl.end()+1;
    simboly = String::from_utf8(sbl.as_bytes().to_vec()).unwrap();
  }

  else{
    let cap = capture.name("End").unwrap();
    
    pos = ltypes::Position::End ;
    
    ind_chr = cap.end();
    simboly = String::from_utf8(cap.as_bytes().to_vec()).unwrap();
    
  }

  if let Some(kind) = class.get_simboly(&simboly){
    if kind == ltypes::TypesObject::Sections(ltypes::TypesSection::Comment){
      
      let (stext, etext) = text.split_at(ind_chr);

      if etext.replace(" ", "").len() > 0{
        if let Some(ltypes::Token::Object(cnt)) = lexer::main(&etext.to_string(), index){
          content = cnt.content;
          pos = ltypes::Position::Inline;
        }
      }

      else{
        content = Some(stext.to_string().drain(..stext.len()-2).collect());

      }
    }

    return Some( ltypes::Token::Object( ltypes::Object{
      line : index,
      kind : kind,
      postion : pos,
      content : content
    }))

  }
  
  println!("not in data base of Simbolys Objects : {simboly}");
  return None;
  
}

pub fn create_linedata(capture : Captures, index : usize, ldtype : ltypes::TypesLineData) -> Option<ltypes::Token>{

  return Some(
    ltypes::Token::LineData(
      ltypes::LineData{
        line  : index,
        kind  : ldtype,
        key   : String::from_utf8(capture.name("Key").unwrap().as_bytes().to_vec()).unwrap(),
        value : DataValue::new(String::from_utf8(capture.name("Value").unwrap().as_bytes().to_vec()).unwrap()),
  
      }
    )
  );
}