//===----------------------------------------------------------------------===//
//
// This source file is part of the Swift.org open source project
//
// Copyright (c) 2014 - 2023 Apple Inc. and the Swift project authors
// Licensed under Apache License v2.0 with Runtime Library Exception
//
// See https://swift.org/LICENSE.txt for license information
// See https://swift.org/CONTRIBUTORS.txt for the list of Swift project authors
//
//===----------------------------------------------------------------------===//

import SwiftSyntax
import SyntaxSupport
import SwiftSyntaxBuilder
import Utils

let syntaxExpressibleByStringInterpolationConformancesFile = SourceFileSyntax(leadingTrivia: copyrightHeader) {
  DeclSyntax("import SwiftSyntax")

  for node in SYNTAX_NODES where node.parserFunction != nil {
    DeclSyntax("extension \(node.kind.syntaxType): SyntaxExpressibleByStringInterpolation {}")
  }

  // `SyntaxParsable` conformance for collection nodes is hand-written.
  // We also need to hand-write the corresponding `SyntaxExpressibleByStringInterpolation` conformances.
  DeclSyntax("extension AccessorDeclListSyntax: SyntaxExpressibleByStringInterpolation {}")
  DeclSyntax("extension AttributeListSyntax: SyntaxExpressibleByStringInterpolation {}")
  DeclSyntax("extension CodeBlockItemListSyntax: SyntaxExpressibleByStringInterpolation {}")
  DeclSyntax("extension MemberBlockItemListSyntax: SyntaxExpressibleByStringInterpolation {}")
}
