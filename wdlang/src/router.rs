use std::path::PathBuf;
use crate::gramma;

pub const ROOT_WD : &str = ".";
pub const SEP_WD : &str = ".";

pub fn main( path : & PathBuf, base_fnc : PathBuf, name_master : String, op_master : Option<&gramma::gtypes::Repository>) -> Vec<gramma::gtypes::WdTemplate>{
  // identify path type
  // for file type execute gramma
  // for dir type do recursive method
  
  let mut data : Vec<gramma::gtypes::WdTemplate> = Vec::new();
  let (templ , repo) = gramma::main(path.join("__init__.wd"), &base_fnc, &name_master, op_master);

  for i in path.read_dir().expect(&format!("error on read dir Pages : {}", path.display())){
    if let Ok(entry) = i{
      let entry_path = entry.path();

      if entry_path.is_file() && entry_path.file_name().unwrap().to_str().unwrap() != "__init__.wd"{
        data.push(gramma::main(entry_path, &base_fnc, &name_master, Some(&repo)).0);

      }

      else if entry_path.is_dir(){
        let name = entry_path.file_name().unwrap().to_str().unwrap();
        let mut data_new = main(&entry_path, base_fnc.join(name.to_string()), name_master.clone() + SEP_WD + name, Some(&repo));
        data.append(& mut data_new);

      }
    }
  }

  data.push(templ);

  return data;

}