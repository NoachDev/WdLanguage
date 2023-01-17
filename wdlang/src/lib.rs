use pyo3::{prelude::*, exceptions::PyTypeError};

use std::{
  path::{
    Path, PathBuf
  }
};

pub mod router;
pub mod gramma;
pub mod lexer;

#[pyfunction]
fn dicovery_dir(main: &str) -> PyResult<Vec<gramma::gtypes::WdTemplate>>{
  let main_path   : &Path   = Path::new(main);
  let wd_pages    : PathBuf = main_path.join("Pages");
  let wd_funct    : PathBuf = main_path.join("Functions");
  // let wd_imags    : PathBuf = main_path.join("Images");
  // let wd_fonts    : PathBuf = main_path.join("Fonts");
  
  if wd_pages.exists() && wd_funct.exists(){
    return Ok(router::main(& wd_pages, wd_funct, String::new()));
  }

  PyResult::Err(PyTypeError::new_err({
    let mut a = "error on get direcorys bases :".to_string();
    
    if wd_pages.exists() == false{
      a += format!(" pages path {}", wd_pages.display()).as_str()
    }
    if wd_funct.exists() == false{
      a += format!(" function path {}", wd_funct.display()).as_str()
    }

  }))


}

/// A Python module implemented in Rust.
#[pymodule]
fn wdlang(_py: Python, m: &PyModule) -> PyResult<()> {
  m.add_function(wrap_pyfunction!(dicovery_dir, m)?)?;

  Ok(())
}