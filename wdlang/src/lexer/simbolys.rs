use super::ltypes;
use lazy_static::lazy_static;
use pcre2::bytes::{RegexBuilder, Regex};


const SECTIONS : [(&str, &str, ltypes::TypesObject); 5] = [
  ("<", ">", ltypes::TypesObject::Sections(ltypes::TypesSection::Widget)),
  ("&", "&", ltypes::TypesObject::Sections(ltypes::TypesSection::Method)),
  ("-", "-", ltypes::TypesObject::Sections(ltypes::TypesSection::Wdvar)),
  (".", ".", ltypes::TypesObject::Sections(ltypes::TypesSection::Preset)),
  ("*", "*", ltypes::TypesObject::Sections(ltypes::TypesSection::Comment))
];

const SEGMENTS : [(&str, &str, ltypes::TypesObject); 3] = [
  ("{", "}", ltypes::TypesObject::Segments(ltypes::TypesSegment::Atributs)),
  ("[", "]", ltypes::TypesObject::Segments(ltypes::TypesSegment::Commands)),
  ("_", "_", ltypes::TypesObject::Segments(ltypes::TypesSegment::Layouts)),
];

pub const DATA_TYPE_SEP : &str = "|"  ;

pub const OBJECTS_ADD   : &str = "|"  ;
pub const LDATA_SEP     : &str = ":"  ;

pub const GLOBAL_START  : &str = "@[(]" ;
pub const GLOBAL_END    : &str = ")"  ;

lazy_static!{
  pub static ref SBL_SECTIONS   : SimbolysObjects = SimbolysObjects::new(&SECTIONS);
  pub static ref SBL_SEGMENTS   : SimbolysObjects = SimbolysObjects::new(&SEGMENTS);
}

lazy_static!{
  static ref STR_SECTIONS   : String  = format!("((\"\"\".*?\"\"\"|\"\".*?\"\"|\".*?\"))(*SKIP)(*FAIL)|((?P<Start>[{}])(?:[{}])|(?:[{}])(?P<End>[{}]))", SBL_SECTIONS.starts, OBJECTS_ADD, OBJECTS_ADD, SBL_SECTIONS.ends);
  static ref STR_SEGMENTS   : String  = format!("((\"\"\".*?\"\"\"|\"\".*?\"\"|\".*?\"))(*SKIP)(*FAIL)|((?P<Start>[{}])(?:[{}])|(?:[{}])(?P<End>[{}]))", SBL_SEGMENTS.starts, OBJECTS_ADD, OBJECTS_ADD, SBL_SEGMENTS.ends) ;
  
  static ref STR_LD_LOCAL   : String  = format!(r"(?P<Key>\w+)(?:[ ]*?){}(?:[ ]*?)(?P<Value>.*)", LDATA_SEP);
  static ref STR_LD_GLOBAL  : String  = format!(r"(?<={})(\s*(?'Key'\w+)\s*[{}]\s*(?'Value'.*?))(?=[{}])", GLOBAL_START, LDATA_SEP, GLOBAL_END);
}

lazy_static!{
  // RegexBuilder::new().build(r"(?P<LineData>(?P<Key>\w+)(?:[ ]*?):(?:[ ]*?)(?P<Value>.*))").unwrap()
  pub static ref PATTERNS       : [(&'static str, Regex, Option<&'static SimbolysObjects>); 4] = [
    ("Object" , RegexBuilder::new().build(&STR_SECTIONS).unwrap() , SBL_SECTIONS.transform()),
    ("Object" , RegexBuilder::new().build(&STR_SEGMENTS).unwrap() , SBL_SEGMENTS.transform()),
    ("Global" , RegexBuilder::new().build(&STR_LD_GLOBAL).unwrap(), None),
    ("Local"  , RegexBuilder::new().build(&STR_LD_LOCAL).unwrap() , None),
  ];
}

lazy_static!{
  pub static ref WORD_IDF : Regex = RegexBuilder::new().build(
    "(?P<quoted>\"\"\".*?\"\"\"|\"\".*?\"\"|\".*?\")|(?P<word>\\w+[.]\\w+|\\w+)|(?P<Cap>.)"
  ).unwrap();

  pub static ref BROKEN_CH  : Regex = RegexBuilder::new().build( "([\\\"\\\'\\{{\\[\\(].+?[\\)\\]\\}}\\\'\\\"])|(?P<End>[,])").unwrap();

  pub static ref GET_KW  : Regex = RegexBuilder::new().build(
    &format!(
      r"^(?(?!(?:[ ].*?){{.*)(:?[ ]*?)(?P<Key>\w+)(?:[ ]*?){}(?:[ ]*?)(?P<Value>.*))$",
      LDATA_SEP
    )
  ).unwrap();

}


#[derive(Debug, PartialEq)]
pub struct SimbolyObject{
  pub start : String,    // expl < | (
  pub end   : String,    // expl > | )
  pub stype : ltypes::TypesObject
}

#[derive(Debug, PartialEq)]
pub struct SimbolysObjects{
  pub starts  : String,
  pub ends    : String,
  pub sblobj  : Vec<SimbolyObject>,
}

impl SimbolysObjects{
  fn transform(&'static self) -> Option<&'static SimbolysObjects>{
    return Some(self);
  }

  pub fn get_simboly(&self, sbl : &String) -> Option<&SimbolyObject>{

    for i in self.sblobj.iter(){
      if &i.start == sbl || &i.end == sbl{
        return Some(i)
      }
    }

    return None;
  }

  pub fn new(sbl : &[(&str, &str, ltypes::TypesObject)]) -> Self{
    let mut ret     : Vec<SimbolyObject> = Vec::new();
    let mut starts  : String = String::new();
    let mut ends    : String = String::new();

    for (start, end, stype) in sbl{
      ret.push(
        SimbolyObject{ start: start.to_string(), end: end.to_string(), stype: *stype }
      );

      starts.push_str(&("\\".to_owned() + start));
      ends.push_str(&("\\".to_owned() + end));
    }

    Self {
      starts:starts,
      ends: ends,
      sblobj: ret
    }
  }
  
}
