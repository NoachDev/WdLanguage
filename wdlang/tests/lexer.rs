use wdlang::lexer::{ltypes::{ Token, Object, TypesObject, TypesSection, TypesSegment, Position::{Start, End, Inline}, LineData, TypesLineData, DataValue}, self};

#[test]
fn lexer_objects(){
  let texts : Vec<(Object, &str)>= vec![
    (Object{line : 0, kind : TypesObject::Sections(TypesSection::Widget), postion : Start, content : None}, "<|"),
    (Object{line : 0, kind : TypesObject::Sections(TypesSection::Widget), postion : End, content : None}, "|>"),

    (Object{line : 0, kind : TypesObject::Sections(TypesSection::Wdvar), postion : Start, content : None}, "-|"),
    (Object{line : 0, kind : TypesObject::Sections(TypesSection::Wdvar), postion : End, content : None}, "|-"),
    
    (Object{line : 0, kind : TypesObject::Sections(TypesSection::Preset), postion : Start, content : None}, ".|"),
    (Object{line : 0, kind : TypesObject::Sections(TypesSection::Preset), postion : End, content : None}, "|."),

    (Object{line : 0, kind : TypesObject::Sections(TypesSection::Method), postion : Start, content : None}, "&|"),
    (Object{line : 0, kind : TypesObject::Sections(TypesSection::Method), postion : End, content : None}, "|&"),

    (Object{line : 0, kind : TypesObject::Sections(TypesSection::Comment), postion : Start, content : None}, "*|"),
    (Object{line : 0, kind : TypesObject::Sections(TypesSection::Comment), postion : End, content : None}, "|*"),
    (Object{line : 0, kind : TypesObject::Sections(TypesSection::Comment), postion : Inline, content : Some(" test ".to_string())}, "*| test |*"),
    (Object{line : 0, kind : TypesObject::Sections(TypesSection::Comment), postion : Inline, content : Some(" *| any |> wd -| vrs |- prs ".to_string())}, "*| *| any |> wd -| vrs |- prs |*"),
    (Object{line : 0, kind : TypesObject::Sections(TypesSection::Comment), postion : Inline, content : Some(" wd_name : test a ".to_string())}, "*| wd_name : test a |*"),

    (Object{line : 0, kind : TypesObject::Segments(TypesSegment::Atributs), postion : Start, content : None}, "{|"),
    (Object{line : 0, kind : TypesObject::Segments(TypesSegment::Atributs), postion : End, content : None}, "|}"),

    (Object{line : 0, kind : TypesObject::Segments(TypesSegment::Commands), postion : Start, content : None}, "[|"),
    (Object{line : 0, kind : TypesObject::Segments(TypesSegment::Commands), postion : End, content : None}, "|]"),
    
    (Object{line : 0, kind : TypesObject::Segments(TypesSegment::Layouts), postion : Start, content : None}, "_|"),
    (Object{line : 0, kind : TypesObject::Segments(TypesSegment::Layouts), postion : End, content : None}, "|_"),

  ];

  for (esp, text) in texts.iter(){
    let tkn = lexer::main(&text.to_string(), 0).unwrap();

    if let Token::Object(obj) = tkn {
      assert_eq!(obj, *esp);
    }
    else {
      panic!("has created {:?}", tkn)
    }

  }

}

#[test]
fn lexer_ldatas(){
  let texts : Vec<(LineData, &str)> = vec![
    (LineData{line : 0, kind : TypesLineData::Local, key : "test".to_string(), value : DataValue::new(" abc".to_string())}, " test : abc"),
    (LineData{line : 0, kind : TypesLineData::Local, key : "test01".to_string(), value : DataValue::new(" {test : \"<|\", test1 : \"|-\", (abc, xyz)} | kwarg : value , kwarg1 : \"[test, second, 1]\", kwarg2 : and".to_string())}, " test01 : {test : \"<|\", test1 : \"|-\", (abc, xyz)} | kwarg : value , kwarg1 : \"[test, second, 1]\", kwarg2 : and"),
    (LineData{line : 0, kind : TypesLineData::Global, key : "test".to_string(), value : DataValue::new("500, 0, testb".to_string())}, "  @(test : 500, 0, testb)"),
  ];
  
  for (esp, text) in texts.iter(){
    let tkn = lexer::main(&text.to_string(), 0).unwrap();

    if let Token::LineData(ldata) = tkn {
      assert_eq!(ldata, *esp);
    }
    else {
      panic!("has created {:?}", tkn)
    }

  }

}