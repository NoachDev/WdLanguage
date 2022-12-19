use std::path::PathBuf;

pub struct WdTemplate{
  name    : String,

  widgets : String,
  wd_vars : String,
  presets : String,
  methods : String,

  script  : PathBuf
}

pub fn main( path : & PathBuf, base_fnc : & PathBuf, data : & mut Vec<WdTemplate>){
  println!("in main router");

  for i in path.read_dir().expect(&format!("error on read dir Pages : {}", path.display())){
    if let Ok(entry) = i{
      let entry_path = entry.path();

      if entry_path.is_file(){
        println!("this is entry : {:?}", entry_path)
      }

      else{
        main(&entry_path, base_fnc, data)
      }
    }
  }

}