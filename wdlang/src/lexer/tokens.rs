use pcre2::bytes::Captures;
use crate::lexer;

use super::{*, ltypes::DataValue};

pub fn create_object(capture : Captures, index : usize, class : &simbolys::SimbolysObjects, mut text : String ) -> Option<ltypes::Token>{
  
  let mut content : Option<String> = None;
  let mut pos : ltypes::Position;

  let simboly : String;

  let mut ind_chr : usize = 0;

  if let Some(sbl) = capture.name("Start"){
    pos = ltypes::Position::Start ;
    ind_chr = sbl.end()+1;
    simboly = String::from_utf8(sbl.as_bytes().to_vec()).unwrap();
  }

  else{
    let cap = capture.name("End").unwrap();
    pos = ltypes::Position::End ;
    simboly = String::from_utf8(cap.as_bytes().to_vec()).unwrap();
  }

  if let Some(sbl_o) = class.get_simboly(&simboly){

    if sbl_o.stype == lexer::ltypes::TypesObject::Sections(lexer::ltypes::TypesSection::Comment) && pos == ltypes::Position::Start{
      let mut after = text.split_off(ind_chr);

      if let Some(ci) = after.rfind(sbl_o.end.as_str()){
        content = Some(after.drain(..ci-1).collect());
        pos = ltypes::Position::Inline;

      }
      
    }

    return Some( ltypes::Token::Object( ltypes::Object{
      line : index,
      kind : sbl_o.stype,
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