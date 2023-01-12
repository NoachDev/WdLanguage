pub mod ltypes;
pub mod simbolys;
mod tokens;

pub fn main(text : &String, index  : usize) -> Option<ltypes::Token>{
  // identify patterns
  // debug ( waring ) unreconizied patterns
  // crete tokens

  for (name , regex, class) in simbolys::PATTERNS.iter() {
    let capture = regex.captures(text.as_bytes()).unwrap();

    if let Some(cap_m) = capture{

      match *name{
        "Object" => return tokens::create_object(cap_m, index, class.unwrap(), text.clone()),
        "Global" => return tokens::create_linedata(cap_m, index, ltypes::TypesLineData::Global),
        "Local"  => return tokens::create_linedata(cap_m, index, ltypes::TypesLineData::Local),
        _ => ()

      }

    }
  }

  // Debug (waring) here

  return None;

}