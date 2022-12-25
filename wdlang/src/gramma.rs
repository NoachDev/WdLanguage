use std::{
  path::PathBuf,
  fs::File,
  io::{
    BufReader, prelude::*
  }
};

use crate::lexer;
pub mod gtypes;

pub fn main(path : PathBuf, base_fnc : &PathBuf) -> gtypes::WdTemplate{
  // path ??(/home/user/project/Pages/__init__.wd ) // encoded utf-8 (ascii)
  // from path read line 
  // get tokens from line 
  // create scopes from tokens 
  // create sub scopes from scopes
  // create elements from scopes and sub scopes

  let templ : gtypes::WdTemplate = gtypes::WdTemplate::new(&path, base_fnc);
  let scopes: Vec<String> = Vec::new();

  let file : File = File::open(&path).expect(&format!("error on read : {}", path.display()));
  let buffer : BufReader<&File> = BufReader::new(&file);

  for (index, line) in buffer.lines().enumerate(){

    // need create comment scope
    let text : String = line.unwrap();
    
    let token : Option<lexer::ltypes::Token> = lexer::main(text, index);
    // println!("my tokens is  {:?}", token);

  }

  return templ;

}