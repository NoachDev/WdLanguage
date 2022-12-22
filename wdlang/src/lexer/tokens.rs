use regex::Captures;
use crate::lexer;

use super::{*, ltypes::DataValue};

pub fn create_object(capture : Captures, index : usize, class : simbolys::SimbolysObjects, mut text : String ) -> Option<ltypes::Token>{
  
  let mut content : Option<String> = None;
  let mut pos : ltypes::Position;

  let simboly : &str;

  let ind_chr : usize;


  if let Some(sbl) = capture.name("Start"){
    
    pos = ltypes::Position::Start ;
    
    ind_chr = sbl.end()+1;
    simboly = sbl.as_str() ;
  }

  else{
    let cap = capture.name("End").unwrap();
    
    pos = ltypes::Position::End ;
    
    ind_chr = cap.end();
    simboly = cap.as_str();

  }

  if let Some(kind) = class.get_simboly(simboly){
    if kind == ltypes::TypesObject::Sections(ltypes::TypesSection::Comment){
      
      let (stext, etext) = text.split_at(ind_chr);

      if etext.replace(" ", "").len() > 0{
        if let Some(ltypes::Token::Object(cnt)) = lexer::main(etext.to_string(), index){
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
  
  return None;
  
}

pub fn create_linedata(capture : Captures, index : usize, ldtype : ltypes::TypesLineData) -> Option<ltypes::Token>{

  return Some(
    ltypes::Token::LineData(
      ltypes::LineData{
        line  : index,
        kind  : ltypes::TypesLineData::Local,
        key   : capture.name("Key").unwrap().as_str().to_string(),
        value : DataValue::new(capture.name("Value").unwrap().as_str().to_string()),
  
      }
    )
  );
}