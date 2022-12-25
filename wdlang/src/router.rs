use std::path::PathBuf;
use crate::gramma;

pub fn main( path : & PathBuf, base_fnc : PathBuf) -> Vec<gramma::gtypes::WdTemplate>{
  // identify path type
  // for file type execute gramma
  // for dir type do recursive method

  let mut data : Vec<gramma::gtypes::WdTemplate> = Vec::new();

  for i in path.read_dir().expect(&format!("error on read dir Pages : {}", path.display())){
    if let Ok(entry) = i{
      let entry_path = entry.path();

      if entry_path.is_file(){
        data.push(gramma::main(entry_path, &base_fnc));

      }

      else{
        let mut data_new = main(&entry_path, base_fnc.join(entry_path.file_name().unwrap().to_str().unwrap().to_string()));
        // data.append(data_new)
        data.append(& mut data_new);

      }
    }
  }

  return data;

}