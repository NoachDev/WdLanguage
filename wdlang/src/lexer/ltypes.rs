use std::{collections::HashMap};
use pyo3::PyAny;
// use regex::Regex;

#[derive(Debug)]
pub enum Position{ Start, End, Inline }

#[derive(Debug, Copy, Clone, PartialEq)]
pub enum TypesSection{ Comment, Widget, Preset, Method, Wdvar }

#[derive(Debug, Copy, Clone, PartialEq)]
pub enum TypesSegment{ Atributs, Commands, Layouts }

#[derive(Debug, Copy, Clone, PartialEq)]
pub enum TypesLineData{ Local, Global }

#[derive(Debug, Copy, Clone, PartialEq)]
pub enum TypesObject{
  Sections(TypesSection),
  Segments(TypesSegment)
}

#[derive(Debug)]
pub struct Object{
  pub line    : usize,
  pub kind    : TypesObject,
  pub postion : Position,
  pub content : Option<String>
}

#[derive(Debug)]
pub struct DataValue{
  pub args : Option<Box<[PyAny]>>,
  pub kwargs : Option<HashMap<String, PyAny>>
}

#[derive(Debug)]
pub struct LineData{
  pub line    : usize,
  pub kind    : TypesLineData,
  pub key     : String,
  pub value   : DataValue
}

#[derive(Debug)]
pub enum Token{
  Object(Object),
  LineData(LineData),
}

impl DataValue{
  pub fn new(values : String) -> Self{
    fn not_instr(find : &str, text : &String) -> usize{

      return 0;
    }

    let sep_index : usize = not_instr("|", &values);
    let mut args : Option<Box<[PyAny]>> = None;
    let mut kwargs: Option<HashMap<String, PyAny>> = None;

    match sep_index{
      0 => {},
      _ => {
        let (str_args, str_kwargs) = values.split_at(sep_index);

      }
    }

    

    Self {
      args: args,
      kwargs: kwargs
    }

  }
}