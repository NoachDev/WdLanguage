use std::{collections::HashMap};
use pyo3::PyAny;

use crate::lexer::simbolys;
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
    fn not_instr(text : &String) -> usize{
      for i in simbolys::FIND_SEP.captures_iter(text.as_bytes()){
        let cap = i.unwrap();
        
        if let Some(find_match) = cap.name("Cap"){
          return find_match.start();

        }
        else if let Some(find_match) = cap.name("kwargs"){
          return 0;
        }
      } 

      return text.len();
    }

    fn create_kwargs() -> Option<HashMap<String, PyAny>>{

      return None;
    }

    fn create_args() -> Option<Box<[PyAny]>>{
      return  None;
    }

    let sep_index : usize = not_instr(&values);
    let mut args : Option<Box<[PyAny]>> = None;
    let mut kwargs: Option<HashMap<String, PyAny>> = None;

    match sep_index{
      0 => {
        println!("my text kw  : {}", &values);
        kwargs = create_kwargs();
      },
      x if x == values.len() => {
        println!("my text arg : {}", &values);
        args = create_args();
        
      },
      _ => {
        let (str_args, str_kwargs) = values.split_at(sep_index);

        println!("my text sep  : {}", &values);
        println!("my index sep : {sep_index}");

        kwargs = create_kwargs();
        args = create_args();

      }
    }

    Self {
      args: args,
      kwargs: kwargs
    }

  }
}