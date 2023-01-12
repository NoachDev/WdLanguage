use std::{
  path::PathBuf,
  fs::File,
  io::{
    BufReader, prelude::*
  }
};

use crate::lexer;

pub mod gtypes;
mod scopes;

pub fn main(path : PathBuf, base_fnc : &PathBuf, master : &String) -> gtypes::WdTemplate{
  // path ??(/home/user/project/Pages/__init__.wd ) // encoded utf-8 (ascii)
  // from path read line 
  // get tokens from line 
  // create scopes from tokens 
  // create sub scopes from scopes
  // create elements from scopes and sub scopes

  let mut templ : gtypes::WdTemplate = gtypes::WdTemplate::new(&path, base_fnc, master);
  let mut manager : scopes::ScopesManager = scopes::ScopesManager::new(&mut templ);

  let file : File = File::open(&path).expect(&format!("error on read : {}", path.display()));
  let buffer : BufReader<&File> = BufReader::new(&file);

  for (index, line) in buffer.lines().enumerate(){
    let text : String = line.unwrap();
    
    if let Some(token) = lexer::main(&text, index){
      if manager.from_token(token).is_comment{
        manager.append_comment(text)
      }

    }
  
  }

  return templ;

}