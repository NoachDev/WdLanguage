use pyo3::prelude::*;

use std::{
  path::{
    Path, PathBuf
  }
};

mod router;
mod gramma;

#[pyfunction]
fn dicovery_dir(main: &str) -> PyResult<&str> {
  let main_path   : &Path   = Path::new(main);
  let wd_pages    : PathBuf = main_path.join("Pages");
  let wd_funct    : PathBuf = main_path.join("Functions");
  // let wd_imags    : PathBuf = main_path.join("Images");
  // let wd_fonts    : PathBuf = main_path.join("Fonts");

  let mut wd_templates : Vec<router::WdTemplate> = Vec::new();
  
  // println!("main  path : {:?}", main_path);
  // println!("pages path : {:?}, exist : {}", wd_pages, wd_pages.exists());
  // println!("funct path : {:?}, exist : {}", wd_funct, wd_funct.exists());

  if wd_pages.exists() && wd_funct.exists(){
    router::main(& wd_pages, wd_funct, & mut wd_templates)
  }

  Ok("")
}

/// A Python module implemented in Rust.
#[pymodule]
fn wdlang(_py: Python, m: &PyModule) -> PyResult<()> {
  m.add_function(wrap_pyfunction!(dicovery_dir, m)?)?;

  Ok(())
}