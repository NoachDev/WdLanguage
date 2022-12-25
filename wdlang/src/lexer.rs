use regex::Regex;

pub mod ltypes;
mod simbolys;
mod tokens;

pub fn main(text : String, index  : usize) -> Option<ltypes::Token>{
  // identify patterns
  // debug ( waring ) unreconizied patterns
  // crete tokens

  let sbl_sections  : simbolys::SimbolysObjects = simbolys::SimbolysObjects::new(&simbolys::SECTIONS);
  let sbl_segments  : simbolys::SimbolysObjects = simbolys::SimbolysObjects::new(&simbolys::SEGMENTS);

  let str_sections  : String  = format!(r"(?P<Start>[{}])(?:[{}])|(?:[{}])(?P<End>[{}])", &sbl_sections.starts, simbolys::OBJECTS_ADD, simbolys::OBJECTS_ADD, &sbl_sections.ends) ;
  let str_segments  : String  = format!(r"(?P<Start>[{}])(?:[{}])|(?:[{}])(?P<End>[{}])", &sbl_segments.starts, simbolys::OBJECTS_ADD, simbolys::OBJECTS_ADD, &sbl_segments.ends) ;

  let str_ld_local  : String  = format!(r"(?P<LineData>(?P<Key>\w+)(?:[ ]*?){}(?:[ ]*?)(?P<Value>.*))", simbolys::LDATA_SEP);
  let str_ld_global : String  = format!(r"(?:{})(?:[ ]*?)(?P<Key>\w+)(?:[ ]*?){}(?:[ ]*?)(?P<Value>.*?)(?:{})", simbolys::GlOBAL_START, simbolys::LDATA_SEP, simbolys::GlOBAL_END);

  let patterns : [(&str, Regex,Option<simbolys::SimbolysObjects>); 4] = [
    ("Local" , Regex::new(&str_ld_local).unwrap(), None),
    ("Object", Regex::new(&str_sections).unwrap(), Some(sbl_sections)),
    ("Object", Regex::new(&str_segments).unwrap(), Some(sbl_segments)),
    ("Global", Regex::new(&str_ld_global).unwrap(), None),
  ];

  for (name , pattern, class) in patterns{
    let capture = pattern.captures(&text);

    if let Some(cap_m) = capture{

      match name{
        "Local"  => return tokens::create_linedata(cap_m, index, ltypes::TypesLineData::Local),
        "Object" => return tokens::create_object(cap_m, index, class.unwrap(), text.clone()),
        "Global" => return tokens::create_linedata(cap_m, index, ltypes::TypesLineData::Global),
        _ => ()

      }

    }
  }

  // Debug (waring) here

  return None;

}