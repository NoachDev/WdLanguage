use std::{
  path::PathBuf,
  fs::File,
  io::{
    BufReader, prelude::*
  }
};

use crate::router::WdTemplate;
use crate::lexer;

mod gtypes;

pub fn main(path : PathBuf, template : WdTemplate){
  // path ??(/home/user/project/Pages/__init__.wd ) // encoded utf-8 (ascii)
  // from path read line 
  // get tokens from line 
  // create scopes from tokens 
  // create sub scopes from scopes
  // create elements from scopes and sub scopes

  let scopes: Vec<String> = Vec::new();

  let file = File::open(&path).expect(&format!("error on read : {}", path.display()));
  let buffer = BufReader::new(&file);

  for (index, line) in buffer.lines().enumerate(){

    // need create comment scope
    let text = line.unwrap();
    
    let token = lexer::main(text, index);
    // println!("my tokens is  {:?}", token);

  }


}