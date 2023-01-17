use std::{collections::HashMap};

use pyo3::{pyclass};

use crate::lexer::simbolys;

#[derive(Debug, PartialEq)]
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

#[derive(Debug, PartialEq)]
pub struct Object{
  pub line    : usize,
  pub kind    : TypesObject,
  pub postion : Position,
  pub content : Option<String>
}

#[pyclass]
#[derive(Debug, Clone, PartialEq)]
pub struct DataValue{
  #[pyo3(get)]
  pub args : Option<Vec<String>>,
  #[pyo3(get)]
  pub kwargs : Option<HashMap<String, String>>
}

#[pyclass]
#[derive(Debug, Clone, PartialEq)]
pub struct LineData{
  #[pyo3(get)]
  pub line    : usize,
  pub kind    : TypesLineData,
  #[pyo3(get)]
  pub key     : String,
  #[pyo3(get)]
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
      } 

      return 0;
    }

    fn broken_in_ch(text : &str) -> Vec<String>{
      let mut start = 0;
      let mut ret : Vec<String> = Vec::new();

      for i in simbolys::BROKEN_CH.captures_iter(text.as_bytes()){
        let cap = i.unwrap();

        if let Some(cap_match) = cap.name("End"){
          ret.push(text[start..cap_match.start()].to_string());
          start = cap_match.end()
        }

      }

      ret.push(text[start..text.len()].to_string());

      // println!("my vec : {:?}", ret);

      return ret;
    }

    fn create_kwargs(ch : &Vec<String>) -> Option<HashMap<String, String>>{
      let mut ret: HashMap<String, String> = HashMap::new();
      let reg = &simbolys::GET_KW;

      for i in ch{
        // println!("my text : {}", i);
        if let Some(cap) = reg.captures(i.as_bytes()).unwrap(){

          let key : String = String::from_utf8_lossy(cap.name("Key").unwrap().as_bytes()).to_string();
          let value : String = String::from_utf8_lossy(cap.name("Value").unwrap().as_bytes()).to_string();

          ret.insert(key, value);
          
        }
        else{
          return None;
        }

      }

      return Some(ret);
    }

    fn create_args(ch : Vec<String>) -> Option<Vec<String>>{
      return Some(ch);
    }

    let sep_index : usize = not_instr(&values);
    let kwargs: Option<HashMap<String, String>>;
    let mut args : Option<Vec<String>> = None;

    match sep_index{
      0 => {
        let ch = broken_in_ch(&values);

        kwargs = create_kwargs(&ch);

        if kwargs.is_none(){
          args = create_args(ch)
        }

      },
      _ => {
        let (str_args, str_kwargs) = values.split_at(sep_index);
        
        kwargs = create_kwargs(&broken_in_ch(&str_kwargs.to_string().strip_prefix("|").unwrap()));
        args = create_args(broken_in_ch(str_args));

      }
    }

    Self {
      args: args,
      kwargs: kwargs
    }

  }
}