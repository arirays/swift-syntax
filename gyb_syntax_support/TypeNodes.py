from .Child import Child
from .Node import Node  # noqa: I201

TYPE_NODES = [
    # simple-type-identifier -> identifier generic-argument-clause?
    Node('SimpleTypeIdentifier', name_for_diagnostics='type', kind='Type',
         children=[
             Child('Name', kind='Token', classification='TypeIdentifier',
                   token_choices=[
                       'IdentifierToken',
                       'KeywordToken',
                       'WildcardToken',
                   ]),
             Child('GenericArgumentClause', kind='GenericArgumentClause',
                   is_optional=True),
         ]),

    # member-type-identifier -> type '.' identifier generic-argument-clause?
    Node('MemberTypeIdentifier', name_for_diagnostics='member type', kind='Type',
         children=[
             Child('BaseType', kind='Type', name_for_diagnostics='base type'),
             Child('Period', kind='PeriodToken'),
             Child('Name', kind='Token',  name_for_diagnostics='name', classification='TypeIdentifier',
                   token_choices=[
                       'IdentifierToken',
                       'KeywordToken',
                   ]),
             Child('GenericArgumentClause', kind='GenericArgumentClause',
                   is_optional=True),
         ]),

    # class-restriction-type -> 'class'
    Node('ClassRestrictionType', name_for_diagnostics=None, kind='Type',
         children=[
             Child('ClassKeyword', kind='KeywordToken', token_choices=['KeywordToken|class']),
         ]),
    # array-type -> '[' type ']'
    Node('ArrayType', name_for_diagnostics='array type', kind='Type',
         children=[
             Child('LeftSquareBracket', kind='LeftSquareBracketToken'),
             Child('ElementType', kind='Type'),
             Child('RightSquareBracket', kind='RightSquareBracketToken'),
         ]),

    # dictionary-type -> '[' type ':' type ']'
    Node('DictionaryType', name_for_diagnostics='dictionary type', kind='Type',
         children=[
             Child('LeftSquareBracket', kind='LeftSquareBracketToken'),
             Child('KeyType', kind='Type', name_for_diagnostics='key type',),
             Child('Colon', kind='ColonToken'),
             Child('ValueType', kind='Type', name_for_diagnostics='value type'),
             Child('RightSquareBracket', kind='RightSquareBracketToken'),
         ]),

    # metatype-type -> type '.' 'Type'
    #                | type '.' 'Protocol
    Node('MetatypeType', name_for_diagnostics='metatype', kind='Type',
         children=[
             Child('BaseType', kind='Type', name_for_diagnostics='base type'),
             Child('Period', kind='PeriodToken'),
             Child('TypeOrProtocol', kind='KeywordToken',
                   token_choices=[
                       'KeywordToken|Type',
                       'KeywordToken|Protocol',
                   ]),
         ]),

    # optional-type -> type '?'
    Node('OptionalType', name_for_diagnostics='optional type', kind='Type',
         children=[
             Child('WrappedType', kind='Type'),
             Child('QuestionMark', kind='PostfixQuestionMarkToken'),
         ]),

    # constrained-sugar-type -> ('some'|'any') type
    Node('ConstrainedSugarType', name_for_diagnostics='type', kind='Type',
         children=[
             Child('SomeOrAnySpecifier', kind='KeywordToken',
                   token_choices=['KeywordToken|some', 'KeywordToken|any']),
             Child('BaseType', kind='Type'),
         ]),

    # implicitly-unwrapped-optional-type -> type '!'
    Node('ImplicitlyUnwrappedOptionalType',
         name_for_diagnostics='implicitly unwrapped optional type', kind='Type',
         children=[
             Child('WrappedType', kind='Type'),
             Child('ExclamationMark', kind='ExclamationMarkToken'),
         ]),

    # composition-type-element -> type '&'
    Node('CompositionTypeElement', name_for_diagnostics=None, kind='Syntax',
         children=[
             Child('Type', kind='Type'),
             Child('Ampersand', kind='Token',
                   is_optional=True),
         ]),

    # composition-typeelement-list -> composition-type-element
    #   composition-type-element-list?
    Node('CompositionTypeElementList', name_for_diagnostics=None,
         kind='SyntaxCollection',
         element='CompositionTypeElement'),

    # composition-type -> composition-type-element-list
    Node('CompositionType', name_for_diagnostics='type composition', kind='Type',
         children=[
             Child('Elements', kind='CompositionTypeElementList',
                   collection_element_name='Element'),
         ]),

    # pack-expansion-type -> type '...'
    Node('PackExpansionType', name_for_diagnostics='variadic expansion', kind='Type',
         children=[
             Child('RepeatKeyword', kind='KeywordToken', token_choices=['KeywordToken|repeat']),
             Child('PatternType', kind='Type')
         ]),

    # pack-reference-type -> 'each' type
    Node('PackReferenceType', name_for_diagnostics='pack reference', kind='Type',
         children=[
             Child('EachKeyword', kind='KeyworkToken',
                   token_choices=['KeywordToken|each'], is_optional=False),
             Child('PackType', kind='Type')
         ]),

    # tuple-type-element -> identifier? ':'? type-annotation ','?
    Node('TupleTypeElement', name_for_diagnostics=None, kind='Syntax',
         traits=['WithTrailingComma'],
         children=[
             Child('InOut', kind='InoutToken',
                   is_optional=True),
             Child('Name', kind='Token', name_for_diagnostics='name',
                   is_optional=True,
                   token_choices=[
                       'IdentifierToken',
                       'WildcardToken'
                   ]),
             Child('SecondName', kind='Token', name_for_diagnostics='internal name',
                   is_optional=True,
                   token_choices=[
                       'IdentifierToken',
                       'WildcardToken'
                   ]),
             Child('Colon', kind='ColonToken',
                   is_optional=True),
             Child('Type', kind='Type'),
             Child('Ellipsis', kind='EllipsisToken',
                   is_optional=True),
             Child('Initializer', kind='InitializerClause',
                   is_optional=True),
             Child('TrailingComma', kind='CommaToken',
                   is_optional=True),
         ]),

    # tuple-type-element-list -> tuple-type-element tuple-type-element-list?
    Node('TupleTypeElementList', name_for_diagnostics=None, kind='SyntaxCollection',
         element='TupleTypeElement'),

    # tuple-type -> '(' tuple-type-element-list ')'
    Node('TupleType', name_for_diagnostics='tuple type', kind='Type',
         traits=['Parenthesized'],
         children=[
             Child('LeftParen', kind='LeftParenToken'),
             Child('Elements', kind='TupleTypeElementList',
                   collection_element_name='Element', is_indented=True),
             Child('RightParen', kind='RightParenToken'),
         ]),

    # throwing-specifier -> 'throws' | 'rethrows'
    # function-type -> attribute-list '(' function-type-argument-list ')'
    #   type-effect-specifiers? return-clause
    Node('FunctionType', name_for_diagnostics='function type', kind='Type',
         traits=['Parenthesized'],
         children=[
             Child('LeftParen', kind='LeftParenToken'),
             Child('Arguments', kind='TupleTypeElementList',
                   collection_element_name='Argument', is_indented=True),
             Child('RightParen', kind='RightParenToken'),
             Child('EffectSpecifiers', kind='TypeEffectSpecifiers',
                   is_optional=True),
             Child('Output', kind='ReturnClause'),
         ]),

    # attributed-type -> type-specifier? attribute-list? type
    # type-specifier -> 'inout' | '__owned' | '__unowned'
    Node('AttributedType', name_for_diagnostics='type', kind='Type',
         traits=['Attributed'],
         children=[
             Child('Specifier', kind='Token',
                   token_choices=['KeywordToken|inout', 'KeywordToken|__shared', 'KeywordToken|__owned', 'KeywordToken|isolated', 'KeywordToken|_const'],
                   is_optional=True),
             Child('Attributes', kind='AttributeList',
                   collection_element_name='Attribute', is_optional=True),
             Child('BaseType', kind='Type'),
         ]),

    # generic-argument-list -> generic-argument generic-argument-list?
    Node('GenericArgumentList', name_for_diagnostics=None, kind='SyntaxCollection',
         element='GenericArgument'),

    # A generic argument.
    # Dictionary<Int, String>
    #            ^~~~ ^~~~~~
    Node('GenericArgument', name_for_diagnostics='generic argument', kind='Syntax',
         traits=['WithTrailingComma'],
         children=[
             Child('ArgumentType', kind='Type'),
             Child('TrailingComma', kind='CommaToken',
                   is_optional=True),
         ]),

    # generic-argument-clause -> '<' generic-argument-list '>'
    Node('GenericArgumentClause', name_for_diagnostics='generic argument clause',
         kind='Syntax',
         children=[
             Child('LeftAngleBracket', kind='LeftAngleToken'),
             Child('Arguments', kind='GenericArgumentList',
                   collection_element_name='Argument'),
             Child('RightAngleBracket', kind='RightAngleToken'),
         ]),

    # named-opaque-return-type -> generic-argument-clause type
    Node('NamedOpaqueReturnType', name_for_diagnostics='named opaque return type', kind='Type',
         children=[
             Child('GenericParameters', kind='GenericParameterClause'),
             Child('BaseType', kind='Type'),
         ]),
]
