use std::path::PathBuf;

pub struct WdTemplate{
  pub name    : String,

  pub widgets : String,
  pub wd_vars : String,
  pub presets : String,
  pub methods : String,

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
      widgets : "".to_string(),
      wd_vars : "".to_string(), // add name
      presets : "".to_string(),
      methods : "".to_string(),
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

        println!("this is entry : {:?}", entry_path)
      }

      else{
        main(&entry_path, base_fnc.join(entry_path.file_name().unwrap().to_str().unwrap().to_string()), data)
      }
    }
  }

}