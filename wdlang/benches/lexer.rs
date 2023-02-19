#![feature(test)]

extern crate test;
use test::Bencher;

use std::{
  path::Path,
  fs::File,
  io::{
    BufReader, prelude::*
  }
};

use wdlang::lexer;

fn lexer_read_file(){
  let file : File = File::open(&Path::new("../App_test/Pages/__init__.wd").to_path_buf()).expect("error on open file __init__.wd");
  let buffer : BufReader<&File> = BufReader::new(&file);
  for (index, line) in buffer.lines().enumerate(){
    let text : String = line.unwrap();
    lexer::main(&test::black_box(text), index);
  }
}

#[bench]
fn lexer_long(b: &mut Bencher) {

  b.iter(|| {
    lexer_read_file()
  });
}

#[bench]
fn lexer_short_data(b: &mut Bencher){
  b.iter(|| {
    lexer::main(&test::black_box("test01                : {test : \"<|\", test1 : \"|-\", [abc, xyz]} | kwarg : value , kwarg1 : \"[test, second, 1]\", kwarg2 : and".to_string()), 0)
  })
  
}

#[bench]
fn lexer_short_simboly(b: &mut Bencher){
  b.iter(|| {
    lexer::main(&"<|".to_string(), 0);
  })
}