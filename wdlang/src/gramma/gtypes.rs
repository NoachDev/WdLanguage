use std::path::PathBuf;

pub struct Widget{

}

pub struct WdVars{

}

pub struct Preset{

}

pub struct Method{

}

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
