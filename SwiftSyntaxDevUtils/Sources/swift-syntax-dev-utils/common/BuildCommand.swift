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

import Foundation

protocol BuildCommand {
  var arguments: BuildArguments { get }
}

extension BuildCommand {
  func buildProduct(productName: String) throws {
    logSection("Building product " + productName)
    try build(packageDir: Paths.packageDir, name: productName, isProduct: true)
  }

  func buildTarget(packageDir: URL, targetName: String) throws {
    logSection("Building target " + targetName)
    try build(packageDir: packageDir, name: targetName, isProduct: false)
  }

  func buildExample(exampleName: String) throws {
    logSection("Building example " + exampleName)
    try build(packageDir: Paths.examplesDir, name: exampleName, isProduct: true)
  }

  @discardableResult
  func invokeSwiftPM(
    action: String,
    packageDir: URL,
    additionalArguments: [String],
    additionalEnvironment: [String: String]
  ) throws -> String {
    var args = [action]
    args += ["--package-path", packageDir.path]

    if let buildDir = arguments.buildDir?.path {
      args += ["--scratch-path", buildDir]
    }

    #if !canImport(Darwin)
    args += ["--enable-test-discovery"]
    #endif

    if arguments.release {
      args += ["--configuration", "release"]
    }

    if let multirootDataFile = arguments.multirootDataFile?.path {
      args += ["--multiroot-data-file", multirootDataFile]
    }

    if arguments.disableSandbox {
      args += ["--disable-sandbox"]
    }

    if arguments.verbose {
      args += ["--verbose"]
    }

    args += additionalArguments

    let processRunner = ProcessRunner(
      executableURL: arguments.toolchain.appendingPathComponent("bin").appendingPathComponent("swift"),
      arguments: args,
      additionalEnvironment: additionalEnvironment
    )

    let result = try processRunner.run(verbose: arguments.verbose)

    return result.stdout
  }

  private func build(packageDir: URL, name: String, isProduct: Bool) throws {
    let args: [String]

    if isProduct {
      args = ["--product", name]
    } else {
      args = ["--target", name]
    }

    var additionalEnvironment: [String: String] = [:]
    additionalEnvironment["SWIFT_BUILD_SCRIPT_ENVIRONMENT"] = "1"

    if arguments.enableRawSyntaxValidation {
      additionalEnvironment["SWIFTSYNTAX_ENABLE_RAWSYNTAX_VALIDATION"] = "1"
    }

    if arguments.enableTestFuzzing {
      additionalEnvironment["SWIFTPARSER_ENABLE_ALTERNATE_TOKEN_INTROSPECTION"] = "1"
    }

    // Tell other projects in the unified build to use local dependencies
    additionalEnvironment["SWIFTCI_USE_LOCAL_DEPS"] = "1"
    additionalEnvironment["SWIFT_SYNTAX_PARSER_LIB_SEARCH_PATH"] =
      arguments.toolchain
      .appendingPathComponent("lib")
      .appendingPathComponent("swift")
      .appendingPathComponent("macos")
      .path

    try invokeSwiftPM(
      action: "build",
      packageDir: packageDir,
      additionalArguments: args,
      additionalEnvironment: additionalEnvironment
    )
  }
}
