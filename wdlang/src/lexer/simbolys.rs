use super::ltypes;

pub const SECTIONS : [(&str, &str, ltypes::TypesObject); 5] = [
  ("<", ">", ltypes::TypesObject::Sections(ltypes::TypesSection::Widget)),
  ("&", "&", ltypes::TypesObject::Sections(ltypes::TypesSection::Method)),
  ("-", "-", ltypes::TypesObject::Sections(ltypes::TypesSection::Wdvar)),
  (".", ".", ltypes::TypesObject::Sections(ltypes::TypesSection::Preset)),
  ("*", "*", ltypes::TypesObject::Sections(ltypes::TypesSection::Comment))
];

pub const SEGMENTS : [(&str, &str, ltypes::TypesObject); 3] = [
  ("(", ")", ltypes::TypesObject::Segments(ltypes::TypesSegment::Atributs)),
  ("[", "]", ltypes::TypesObject::Segments(ltypes::TypesSegment::Commands)),
  ("_", "_", ltypes::TypesObject::Segments(ltypes::TypesSegment::Layouts)),
];

pub const OBJECTS_ADD   : &str = "|"  ;
pub const LDATA_SEP     : &str = ":"  ;

pub const GlOBAL_START  : &str = "@(" ;
pub const GlOBAL_END    : &str = ")"  ;


#[derive(Debug, PartialEq)]
pub struct SimbolyObject<'a>{
  pub start : &'a str,    // expl < | (
  pub end   : &'a str,    // expl > | )
  pub stype : ltypes::TypesObject
}

#[derive(Debug, PartialEq)]
pub struct SimbolysObjects<'a>{
  pub starts  : String,
  pub ends    : String,
  pub sblobj  : Vec<SimbolyObject<'a>>,
}

impl<'a> SimbolysObjects<'a>{
  pub fn get_simboly(self, sbl : &str) -> Option<ltypes::TypesObject>{

    for i in self.sblobj.iter(){
      if i.start == sbl{
        return Some(i.stype)
      }
      else if i.end == sbl {
        return Some(i.stype)

      }
    }

    return None;
  }

  pub fn new(sbl : &[(&'a str, &'a str, ltypes::TypesObject)]) -> Self{
    let mut ret     : Vec<SimbolyObject> = Vec::new();
    let mut starts  : String = String::new();
    let mut ends    : String = String::new();

    for (start, end, stype) in sbl{
      ret.push(
        SimbolyObject{ start: start, end: end, stype: *stype }
      );

      starts.push_str(start);
      ends.push_str(end);
    }

    Self {
      starts:starts,
      ends: ends,
      sblobj: ret
    }
  }
  
}