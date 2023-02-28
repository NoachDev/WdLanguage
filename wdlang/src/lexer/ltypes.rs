use std::{collections::HashMap};
use pyo3::{pyclass, IntoPy, PyObject, Python};

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

#[derive(Debug, Clone, PartialEq)]
pub struct StringVar{
  variables  : Option<HashMap<usize, (String, String)>>,
  pub content  : String
  
}

#[pyclass]
#[derive(Debug, Clone, PartialEq)]
pub struct DataValue{
  #[pyo3(get)]
  pub args : Option<Vec<StringVar>>,
  #[pyo3(get)]
  pub kwargs : Option<HashMap<String, StringVar>>
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
  pub fn args_list(self) -> Vec<String>{
    self.args.unwrap().iter().map(|x| x.content.to_string()).collect()
  }

  pub fn new(values : String) -> Self{
    fn not_instr(text : &String) -> usize{
      for i in simbolys::WORD_IDF.captures_iter(text.as_bytes()){
        let cap = i.unwrap();
        
        if let Some(find_match) = cap.name("Cap"){
          if String::from_utf8_lossy(find_match.as_bytes()).to_string() == simbolys::DATA_TYPE_SEP{
            return find_match.start();
          }
          
        }
      } 

      return 0;
    }

    fn broken_in_ch(text : &str) -> Vec<StringVar>{
      let mut start = 0;
      let mut ret : Vec<StringVar> = Vec::new();

      for i in simbolys::BROKEN_CH.captures_iter(text.as_bytes()){
        let cap = i.unwrap();

        if let Some(cap_match) = cap.name("End"){
          ret.push(StringVar::new(text[start..cap_match.start()].to_string()));
          start = cap_match.end()
        }

      }
      let strvar = StringVar::new(text[start..text.len()].to_string());

      ret.push(strvar);

      return ret;
    }

    fn create_kwargs(ch : &Vec<StringVar>) -> Option<HashMap<String, StringVar>>{
      let mut ret: HashMap<String, StringVar> = HashMap::new();
      let reg = &simbolys::GET_KW;

      for i in ch{
        if let Some(cap) = reg.captures(i.content.as_bytes()).unwrap(){

          let key : String = String::from_utf8_lossy(cap.name("Key").unwrap().as_bytes()).to_string();
          let value : StringVar = StringVar{
            variables : None,
            content : String::from_utf8_lossy(cap.name("Value").unwrap().as_bytes()).to_string()
          };

          ret.insert(key, value);
          
        }
        else{
          return None;
        }

      }

      return Some(ret);
    }

    fn create_args(ch : Vec<StringVar>) -> Option<Vec<StringVar>>{
      return Some(ch);
    }

    let sep_index : usize = not_instr(&values);
    let kwargs: Option<HashMap<String, StringVar>>;
    let mut args : Option<Vec<StringVar>> = None;

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

impl StringVar{
  pub fn load_vars(& mut self){

    let mut salt : isize = 0;

    if let Some(vars_pool) = self.variables.as_ref(){
      let mut idx = vars_pool.keys().collect::<Vec<&usize>>();
      idx.sort(); 

      for start in idx{
        let (name, content) = vars_pool.get(start).as_ref().unwrap();

        let end = ( start + name.len() ) as isize + salt;

        self.content.replace_range( (*start as isize + salt) as usize .. end as usize, format!("({})", content).as_str());
        
        salt += (content.len() + 2) as isize;
        salt -= name.len() as isize ;

      }
      
    }
    
  }

  pub fn append_vars(& mut self, name : String, change : String, index : usize){

    if self.variables.is_none(){
      self.variables = Some(HashMap::new());
    }

    self.variables.as_mut().unwrap().insert(index, (name, change));

  }
  
  pub fn new(name : String) -> Self{
    Self{
      variables : None,
      content : name
    }
  }
}

impl IntoPy<PyObject> for StringVar {
  fn into_py(self, py: Python<'_>) -> PyObject {
    return self.content.trim().into_py(py);
  }
}
