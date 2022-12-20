use std::{
  path::PathBuf,
  fs::File,
  io::{
    BufReader, prelude::*
  },
};

use crate::router::WdTemplate;
mod gtypes;

pub fn main(path : PathBuf, template : WdTemplate){
  // * path ??(/home/user/project/Pages/__init__.wd ) // encoded utf-8 (ascii)
  // * from path read line 
  // get tokens from line 
  // create scopes from tokens 
  // create sub scopes from scopes
  // create elements from scopes and sub scopes

  let scopes: Vec<String> = Vec::new();

  let file = File::open(&path).expect(&format!("error on read : {}", path.display()));
  let buffer = BufReader::new(&file);

  for line in buffer.lines(){
    let text = line.unwrap();

    // println!("line {}", text);
    // 

  }


}