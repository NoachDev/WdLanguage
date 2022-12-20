use std::path::PathBuf;
use crate::gramma;

pub struct WdTemplate{
  pub name    : String,

  pub widgets : Vec<String>,
  pub wd_vars : Vec<String>,
  pub presets : Vec<String>,
  pub methods : Vec<String>,

  pub script  : Option<PathBuf>
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
      name    : name,
      widgets : Vec::new(),
      wd_vars : Vec::new(), // add name
      presets : Vec::new(),
      methods : Vec::new(),
      script  : script
    
    }
  }
}

pub fn main( path : & PathBuf, base_fnc : PathBuf, data : & mut Vec<WdTemplate>){
  // identify path type
  // for file type execute gramma
  // for dir type do recursive method

  for i in path.read_dir().expect(&format!("error on read dir Pages : {}", path.display())){
    if let Ok(entry) = i{
      let entry_path = entry.path();

      if entry_path.is_file(){
        let templ = WdTemplate::new(path, &base_fnc);

        gramma::main(entry_path, templ);

      }

      else{
        main(&entry_path, base_fnc.join(entry_path.file_name().unwrap().to_str().unwrap().to_string()), data)
      }
    }
  }

}