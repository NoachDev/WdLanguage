#![feature(test)]

extern crate test;
use test::Bencher;

use std::{
  path::{Path, PathBuf},
  env::temp_dir,
  fs::File,
  io::Write
};

use wdlang::gramma;

#[bench]
fn gramma_short_section(b : & mut Bencher){

  let text = "
    -|
      var_gramma            : gramma 1
      var_second            : test_abc
      var_test03            : test_xyz
      var_last              : [1,2,3,4,5]
    |-
  ";
  
  let mut dir_tmp = temp_dir();
  dir_tmp.push("gramma_short_section.wd");

  File::create(&dir_tmp).unwrap().write_all(text.as_bytes());

  b.iter(|| {
    gramma::main(dir_tmp.clone(), &PathBuf::new(), &".".to_string(), None);
  })

}

#[bench]
fn gramma_short_section_segment(b : & mut Bencher){

  let text = "
    <|
      wd_name               : test_gramma
      wd_type               : Label

      {|
        highlightthickness  : 2
        width               : 10
        height              : 5
      |}

      [|
        grid                : row : 0, column : 0
      |]

    |>
  ";
  
  let mut dir_tmp = temp_dir();
  dir_tmp.push("gramma_short_section_segment.wd");

  File::create(&dir_tmp).unwrap().write_all(text.as_bytes());

  b.iter(|| {
    gramma::main(dir_tmp.clone(), &PathBuf::new(), &".".to_string(), None);
  })

}

#[bench]
fn gramma_long_file(b : & mut Bencher){

  b.iter(|| {
    gramma::main(Path::new("../App_test/Pages/__init__.wd").to_path_buf(), &PathBuf::new(), &".".to_string(), None);
  }) 
}