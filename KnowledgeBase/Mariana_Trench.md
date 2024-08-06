# Website

This website is built using [Docusaurus 2](https://v2.docusaurus.io/), a modern static website generator.

### Installation

```
$ yarn
```

### Local Development

```
$ yarn start
```

This command starts a local development server and open up a browser window. Most changes are reflected live without having to restart the server.

### Build

```
$ yarn build
```

This command generates static content into the `build` directory and can be served using any static contents hosting service.

### Deployment

```
$ GIT_USER=<Your GitHub username> USE_SSH=true yarn deploy
```

If you are using GitHub pages for hosting, this command is a convenient way to build the website and push to the `gh-pages` branch.

### Continuous Integration

Some common defaults for linting/formatting have been set for you. If you integrate your project with an open source Continuous Integration system (e.g. Travis CI, CircleCI), you may check for issues using the following command.

```
$ yarn ci
```


---
slug: welcome
title: Welcome
author: Mariana Trench Team
author_title: Mariana Trench Team
author_url: https://github.com/facebook/mariana-trench
author_image_url: https://avatars.githubusercontent.com/u/19538647?v=4
tags: [facebook, hello]
---

First post


---
id: android-lifecycles
title: Android/API Lifcycles
sidebar_label: Android/API Lifcycles
---

import {OssOnly, FbInternalOnly} from 'docusaurus-plugin-internaldocs-fb/internal';
import FbAndroidLifecycles from './fb/android_lifecycles.md';

## Background
Framework classes often provide overridable methods that subclasses can override. These methods are frequently executed in some sequence. The most direct example of this would be the [Activity life-cycle](https://developer.android.com/guide/components/activities/activity-lifecycle). Sub-classes implement methods like onCreate(), onStart(), onResume(), etc. which is internally chained up in the base class.

The analysis may see this chain if the code for the base class is available. However, because the base class can be overridden by many different children, the analysis cannot easily differentiate between flows `Child1.onCreate() -> Child1.onStart()` and `Child1.onCreate() -> Child2.onStart()`. The latter could result in a false positives. There could also be too many children and which causes the analysis to drop taint and fail to find any flow.

To get around this, we allow users to define life-cycles for these framework classes.

## Life-cycle Configuration

<FbInternalOnly> <FbAndroidLifecycles /> </FbInternalOnly>

<OssOnly>

The default life-cycles are defined in [configuration/lifecycles.json](https://github.com/facebook/mariana-trench/blob/main/configuration/lifecycles.json).

</OssOnly>


## Life-cycle Definition
Life-cycles are defined in a JSON file and passed into the analysis via the `--lifecycles-paths` option. Here is a sample definition.

```
  {
    "base_class_name": "Landroidx/fragment/app/FragmentActivity;",
    "method_name": "activity_lifecycle_wrapper",
    "callees": [
      {
        "method_name": "onCreate",
        "return_type": "V",
        "argument_types": [
          "Landroid/os/Bundle;"
        ]
      },
      {
        "method_name": "onStart",
        "return_type": "V",
        "argument_types": []
      }
    ]
  },
```

Most of the fields should be self-explanatory, with just a few additional notes:
* The analysis internally creates artificial methods with signature `<child of base_class_name>.<method_name>(args for callees)` that calls the "callees" in the defined sequence.
* "method_name" must be unique across all life-cycles. Children could extend multiple base classes. If their respective life-cycle definitions share a "method_name", there will be a conflict.
* Only children at the leaves of the class hierarchy will have the artificial method created, so taint flow will only be detected in these classes.


---
id: build-from-source
title: Build from Source
sidebar_label: Build from Source
---

This documentation aims to help you build Mariana Trench from source and run the tests.

## Supported Platforms

Mariana Trench is currently supported on **macOS** (tested on *Big Sur 11.4*) and **Linux** (tested on *Ubuntu 20.04 LTS*).

## Dependencies

Below is a list of the required dependencies. Most of them can be installed with **[Homebrew](https://brew.sh/)**.

* A C++ compiler that supports C++17 (GCC >= 7 or Clang >= 5)
* Python >= 3.6
* CMake >= 3.19.3
* zlib
* Boost >= 1.75.0
* GoogleTest >= 1.10.0
* JsonCpp >= 1.9.4
* fmt >= 7.1.2, <= 8.1.1
* RE2
* Java (Optional)
* Android SDK (Optional)
* Redex (master)

## Building and Installing

### Install all dependencies with Homebrew

First, follow the instructions to install **[Homebrew](https://brew.sh/)** on your system.

Then, make sure homebrew is up-to-date:
```shell
$ brew update
$ brew upgrade
```

Finally, install all the dependencies.

On **macOS**, run:
```shell
$ brew install python3 git cmake zlib boost googletest jsoncpp re2
```

On **Linux**, run:
```shell
$ brew install git cmake zlib boost jsoncpp re2
$ brew install googletest --build-from-source # The package is currently broken.
$ export CMAKE_PREFIX_PATH=/home/linuxbrew/.linuxbrew/opt/jsoncpp:/home/linuxbrew/.linuxbrew/opt/zlib
```

On **Linux**, you will need to install Java to run the tests. For instance, on **Ubuntu**, run:
```shell
$ sudo apt install default-jre default-jdk
```

### Clone the repository

First of, clone the Mariana Trench repository. We will also set an environment variable `MARIANA_TRENCH_DIRECTORY` that points to it for the following instructions.
```shell
$ git clone https://github.com/facebook/mariana-trench.git
$ cd mariana-trench
$ MARIANA_TRENCH_DIRECTORY="$PWD"
```

### Installation directory

We do not recommend installing Mariana Trench as root. Instead, we will install all libraries and binaries in a directory "install".
We will also use a directory called "dependencies" to store dependencies that we have to build from source.
Run the following commands:
```shell
$ mkdir install
$ mkdir dependencies
```

### Building fmt

The 9.0 release of `fmt` has breaking changes that Mariana Trench is not yet compatible with, so for now, you need to build the library from source. You will need to do the following:

```shell
$ cd "$MARIANA_TRENCH_DIRECTORY/dependencies"
$ git clone -b 8.1.1 https://github.com/fmtlib/fmt.git
$ mkdir fmt/build
$ cd fmt/build
$ cmake -DCMAKE_INSTALL_PREFIX="$MARIANA_TRENCH_DIRECTORY/install" ..
$ make -j4
$ make install
```

### Building Redex

We also need to build [Redex](https://fbredex.com/) from source, run:
```shell
$ cd "$MARIANA_TRENCH_DIRECTORY/dependencies"
$ git clone https://github.com/facebook/redex.git
$ mkdir redex/build
$ cd redex/build
$ cmake -DCMAKE_INSTALL_PREFIX="$MARIANA_TRENCH_DIRECTORY/install" ..
$ make -j4
$ make install
```

### Building Mariana Trench

Now that we have our dependencies ready, let's build the Mariana Trench binary:
```shell
$ cd "$MARIANA_TRENCH_DIRECTORY"
$ mkdir build
$ cd build
$ cmake \
  -DREDEX_ROOT="$MARIANA_TRENCH_DIRECTORY/install" \
  -Dfmt_ROOT="$MARIANA_TRENCH_DIRECTORY/install" \
  -DCMAKE_INSTALL_PREFIX="$MARIANA_TRENCH_DIRECTORY/install" \
  ..
$ make -j4
$ make install
```

Finally, let's install Mariana Trench as a Python package.
First, follow the instructions to create a [virtual environment](https://packaging.python.org/tutorials/installing-packages/#creating-virtual-environments).
Once inside a virtual environment (after using the `activate` script), run:
```shell
$ cd "$MARIANA_TRENCH_DIRECTORY"
$ python scripts/setup.py \
  --binary "$MT_INSTALL_DIRECTORY/bin/mariana-trench-binary" \
  --pyredex "$MT_INSTALL_DIRECTORY/bin/pyredex" \
  install
```

## Testing during development

If you are making changes to Mariana Trench, you can use the `mariana-trench` wrapper inside the build directory:
```shell
$ cd build
$ ./mariana-trench --help
```

This way, you don't have to call `scripts/setup.py` between every changes.
Python changes will be automatically picked up.
C++ changes will be picked up after running `make`.

Note that you will need to install all python dependencies:
```shell
$ pip install pyre_extensions fb-sapp
```

## Running the tests

To run the tests after building Mariana Trench, use:
```shell
$ cd build
$ make check
```

## Troubleshooting

Here are a set of errors you might encounter, and their solutions.

### CMake Warning: Ignoring extra path from command line: ".."

You probably tried to run `cmake` from the wrong directory.
Make sure that `$MARIANA_TRENCH_DIRECTORY` is set correctly (test with `echo $MARIANA_TRENCH_DIRECTORY`).
Then, run the instructions again from the beginning of the section you are in.

### error: externally-managed-environment

You probably tried to run `python scripts/setup.py` without a virtual environment. Create a [virtual environment](https://packaging.python.org/tutorials/installing-packages/#creating-virtual-environments) first.

### undefined reference to `pthread_create@GLIBC`

This seems to happen on Linux, when your operating system has an old version of glibc, which doesn't match the version used by Homebrew.
Try upgrading your operating system to the last version.

Another option is to use the compiler (gcc) from Homebrew directly:
```
$ brew install gcc
export CC=/home/linuxbrew/.linuxbrew/bin/cc
export CXX=/home/linuxbrew/.linuxbrew/bin/c++
```
You will need to run all the instructions from this page again, starting from `Clone the repository`. We recommend starting from scratch, i.e delete the mariana-trench directory.


---
id: configuration
title: Analysis Configuration Options
sidebar_label: Analysis Configuration Options
---

Mariana Trench is highly configurable and we recommend that you invest time into adjusting the tool to your specific use cases. At Meta, we have dedicated security engineers that will spend a significant amount of their time adding new rules and model generators to improve the analysis results.

This page will cover the more important, non-trivial configuration options. Note that you will spend most of your time configuring Mariana Trench writing model generators. These are covered in the [Models and Model Generators](models.md).


## Command Line Options

You can get a full set of options by running `mariana-trench --help`. The following is an abbreviated version of the output.
```shell
$ mariana-trench --help

Target arguments:
  --apk-path APK_PATH   The APK to analyze.

Output arguments:
  --output-directory OUTPUT_DIRECTORY
                        The directory to store results in.

Configuration arguments:
  --system-jar-configuration-path SYSTEM_JAR_CONFIGURATION_PATH
                        A JSON configuration file with a list of paths to the system jars.
  --rules-paths RULES_PATHS
                        A `;`-separated list of rules files and directories containing rules files.
  --repository-root-directory REPOSITORY_ROOT_DIRECTORY
                        The root of the repository. Resulting paths will be relative to this.
  --source-root-directory SOURCE_ROOT_DIRECTORY
                        The root where source files for the APK can be found.
  --model-generator-configuration-paths MODEL_GENERATOR_CONFIGURATION_PATHS
                        A `;`-separated list of paths specifying JSON configuration files. Each file is a list of paths to JSON model generators relative to the
                        configuration file or names of CPP model generators.
  --model-generator-search-paths MODEL_GENERATOR_SEARCH_PATHS
                        A `;`-separated list of paths where we look up JSON model generators.
  --maximum-source-sink-distance MAXIMUM_SOURCE_SINK_DISTANCE
                        Limits the distance of sources and sinks from a trace entry point.
  ```

#### `--apk-path`
Mariana Trench analyzes Dalvik bytecode. You provide it with the android app (APK) to analyze.

#### `--output-directory OUTPUT_DIRECTORY`
The output of the analysis is a file containing metadata about the particular run in JSON format as well as sharded files containing data flow specifications for every method in the APK. These files need to be processed by SAPP (see [Getting Started](getting_started.md)) after the analysis. The flag specifies where these files are saved.

#### `--system-jar-configuration-path SYSTEM_JAR_CONFIGURATION_PATH`
This path points to a json file containing a list of `.jar` files that the analysis should include in the analysis. It's important that this contains at least the `android.jar` on your system. This file is typically located in your android SDK distribution at `$ANDROID_SDK/platforms/android-30/android.jar`. Without the `android.jar`, Mariana Trench will not know about many methods from the standard library that might be important for your model generators.

#### `--rules-paths RULES_PATHS`
A `;` separated search path pointing to files and directories containing rules files. These files specify what taint flows Mariana Trench should look for. Check out the [`rules.json`](https://github.com/facebook/mariana-trench/blob/main/configuration/rules.json#L2-L13) that's provided by default. It specifies that we want to find flows from user controlled input (`ActivityUserInput`) into `CodeExecution` sinks and that this constitutes a remote code execution.

#### `--source-root-directory SOURCE_ROOT_DIRECTORY`
Mariana Trench will do a source indexing path before the analysis. This is because Dalvik/Java bytecode does not contain complete location information, only filenames (not paths) and line numbers. The index is later used to emit precise locations.

#### `--model-generator-configuration-paths MODEL_GENERATOR_CONFIGURATION_PATHS`
A `;` separated set of files containing the names of model generators to run. See [`default_generator_config.json`](https://github.com/facebook/mariana-trench/blob/main/configuration/default_generator_config.json) for an example.

#### `--model-generator-search-paths MODEL_GENERATOR_SEARCH_PATHS`
A `;` separated search path where Mariana Trench will try to find the model generators specified in the generator configuration.

#### `--maximum-source-sink-distance MAXIMUM_SOURCE_SINK_DISTANCE`
For performance reasons it can be useful to limit the maximum length of a trace Mariana Trench tries to find (note that longer traces also tend to be harder to interpret). Due to the modular nature of the analysis the value specified here limits the maximum length from the trace root to the source, and from the trace root to the sink. This means found traces can have length of `2 x MAXIMUM_SOURCE_SINK_DISTANCE`.

#### `--heuristics HEURISTICS_FILE_PATH`
Mariana Trench uses various heuristics parameters during the analysis. It is possible to set some of them with a JSON configuration file. The complete list of configurable parameters is reported in the [heuristics parameters section](#heuristics-parameters). It is optional to specify a configuration for the heuristics parameters, and the the parameters that are not specified are set to a default value.

## Heuristics Parameters

#### `join_override_threshold INT`
When a method has a set of overrides greater than this threshold, Mariana Trench does not join all overrides at call sites.

#### `android_join_override_threshold INT`
When an android/java/google method has a set of overrides which is greater than this threshold, Mariana Trench does not join all overrides at call sites.

#### `warn_override_threshold INT`
When a method which has a set of overrides greater than this threshold that is not marked with `NoJoinVirtualOverrides` is called at least once, Mariana Trench prints a warning.

#### `generation_max_port_size INT`
Maximum size of the port of a generation.

#### `generation_max_output_path_leaves INT`
Maximum number of leaves in the tree of output paths of generations. When reaching the maximum, Mariana Trench collapses all the subtrees into a single node.

#### `parameter_source_max_port_size INT`
Maximum size of the port of a parameter source.

#### `parameter_source_max_output_path_leaves INT`
Maximum number of leaves in the tree of output paths of parameter sources. When reaching the maximum, Mariana Trench collapses all the subtrees into a single node.

#### `sink_max_port_size INT`
Maximum size of the port of a sink.

#### `sink_max_input_path_leaves INT`
Maximum number of leaves in the tree of input paths of sinks. When reaching the maximum, Mariana Trench collapses all the subtrees into a single node.

#### `call_effect_source_max_port_size INT`
Maximum size of the port of a call effect source.

#### `call_effect_source_max_output_path_leaves INT`
Maximum number of leaves in the tree of output paths of call effect sources. When reaching the maximum, Mariana Trench collapses all the subtrees into a single node.

#### `call_effect_sink_max_port_size INT`
Maximum size of the port of a call effect sink.

#### `call_effect_sink_max_input_path_leaves INT`
Maximum number of leaves in the tree of input paths of call effect sinks. When reaching the maximum, Mariana Trench collapses all the subtrees into a single node.

#### `max_number_iterations INT`
Maximum number of global iterations before Mariana Trench aborts the analysis.

#### `max_depth_class_properties INT`
Maximum depth of dependency graph traversal to find class properties.

#### `max_call_chain_source_sink_distance INT`
Maximum number of hops that can be tracked for a call chain issue.

#### `propagation_max_input_path_size INT`
Maximum size of the input access path of a propagation.

#### `propagation_max_input_path_leaves INT`
Maximum number of leaves in the tree of input paths of propagations.

### Heuristics Parameter Configuration Example

The following JSON document is a valid configuration file for the heuristics parameters.
Typically, we try to find a balance between precision of the analysis and performance.
```json
{
    "join_override_threshold": 100,
    "android_join_override_threshold": 100,
    "warn_override_threshold": 100,
    "generation_max_port_size": 10,
    "generation_max_output_path_leaves": 30,
    "parameter_source_max_port_size": 10,
    "parameter_source_max_output_path_leaves": 30,
    "sink_max_port_size": 10,
    "sink_max_input_path_leaves": 30,
    "call_effect_source_max_port_size": 10,
    "call_effect_source_max_output_path_leaves": 30,
    "call_effect_sink_max_port_size": 10,
    "call_effect_sink_max_input_path_leaves": 30,
    "max_number_iterations": 300,
    "max_depth_class_properties": 30,
    "max_call_chain_source_sink_distance": 30,
    "propagation_max_input_path_size": 10,
    "propagation_max_input_path_leaves": 10
}
```


---
id: customize-sources-and-sinks
title: Customize Sources and Sinks
sidebar_label: Customize Sources and Sinks
---

import {OssOnly, FbInternalOnly} from 'docusaurus-plugin-internaldocs-fb/internal'; import FbCustomizeSourcesAndSinks from './fb/customize_sources_and_sinks.md';

This page provides a high-level overview of the steps needed to update or create new sources and sinks.

## Overview

Under the context of Mariana Trench, we talk about sources and sinks in terms of methods (or, rarely, fields). For example, we may say that the return value of a method is a source (or a sink). We may also say that the 2nd parameter of a method is a source (or a sink). Such description of a method is called a **"model"**. See [Models & Model Generators](./models.md) for more details about models and writing them.

<FbInternalOnly> <FbCustomizeSourcesAndSinks/> </FbInternalOnly>

<OssOnly>

To define sources or sinks that are not contained in the default set of [sources](https://github.com/facebook/mariana-trench/tree/main/configuration/model-generators/sources) and [sinks](https://github.com/facebook/mariana-trench/tree/main/configuration/model-generators/sinks), a user needs to:

1. Write one or more JSON files that respect our [model generator Domain Specific Language (DSL)](./models.md), which express how to generate models from methods and are hence called **"model generators"**.

   - For example, a model generator may say that, for all methods (that will be analyzed by Mariana Trench) whose name is `onActivityResult`, specify their 2nd parameter as a source.

   ```json
   {
     "model_generators": [
       {
         "find": "methods",
         "where": [
           {
             "constraint": "name",
             "pattern": "onActivityResult"
           }
         ],
         "model": {
           "sources": [
             {
               "kind": "TestSensitiveUserInput",
               "port": "Argument(2)"
             }
           ]
         }
       }
     ]
   }
   ```

2. Instruct Mariana Trench to read from your model generator, so that Mariana Trench will generate models at runtime.
   - Intuitively, the models generated (by interpreting model generators) express sources and sinks for each method **before** running Mariana Trench. Based on such models, Mariana Trench will automatically infer **new** models for each method at runtime.
   - To instruct Mariana Trench to read from customized JSON model generators, add your json model generator [here](https://github.com/facebook/mariana-trench/tree/main/configuration/model-generators).
   - Add the model generator name (i.e, the file name) in the [JSON configuration file](https://github.com/facebook/mariana-trench/blob/main/configuration/default_generator_config.json).
3. Update **"rules"** if necessary.
   - Background: Mariana Trench categorizes sources and sinks into different **"kinds"**, which are string-typed. For example, a source may have a kind of`JavascriptInterfaceUserInput`. A sink may have a kind of `Logging`. Mariana Trench only finds data flow **from sources of a particular kind to sinks of another particular kind**, which are called **"rules"**. See [Rules](./rules.md) for writing them.
   - To specify kinds that are not mentioned in the default set of rules or to specify rules that are different than the default rules, you need to specify a new rule in file [`rules.json`](https://github.com/facebook/mariana-trench/blob/main/configuration/rules.json), in order to instruct Mariana Trench to find data flow that matches the new rule.
   - For example, to catch flows from `TestSensitiveUserInput` in the example above and the sink kind `Logging`, you can add the following rule to the default [`rules.json`](https://github.com/facebook/mariana-trench/blob/main/configuration/rules.json):
   ```json
   {
    "name": "TestRule",
    "code": 18,
    "description": "A test rule",
    "sources": [
      "TestSensitiveUserInput"
    ],
    "sinks": [
      "Logging"
    ]
   }
   ```

</OssOnly>


---
id: debugging-fp-fns
title: Debugging False Positives/False Negatives
sidebar_label: Debugging False Positives/False Negatives
---
import {OssOnly, FbInternalOnly} from 'docusaurus-plugin-internaldocs-fb/internal';
import FbDebugging from './fb/debugging_fp_fns.md';

This document is mainly intended for software engineers, to help them debug false positives and false negatives.

<OssOnly>
## Setup

First, you need to run the analysis on your computer. This will create `model@XXX.json` files in the current directory, containing the results of the analysis.
</OssOnly>
<FbInternalOnly> <FbDebugging/> </FbInternalOnly>

## Investigate the output models

Now, your objective is to understand in which method we lost the flow (false negative) or introduced the invalid flow (false positive). You will need to look into the output models for that. These models include both the declared models and inferred models. Declared models are models explicitly written out or created by a model generator. Inferred models are models created by Mariana Trench's analysis of other models and the code. I recommend using the `explore_models.py` bento script.

Run the following command in the directory containing the output model files (i.e, `model@XXX.json`):
<OssOnly>

```shell
python3 -i mariana_trench_repository/scripts/explore_models.py
```

</OssOnly>
<FbInternalOnly>

```shell
bento console -i --file ~/fbsource/fbandroid/native/mariana-trench/scripts/explore_models.py
```

</FbInternalOnly>

This provides you with a few helper functions:
```shell
  index('.')                    Index all available models in the given directory.
  method_containing('Foo;.bar') Find all methods containing the given string.
  method_matching('Foo.*')      Find all methods matching the given regular expression.
  get_model('Foo;.bar')         Get the model for the given method.
  print_model('Foo;.bar')       Pretty print the model for the given method.
```
Use `index` to index all models first:
```shell
In [1]: index()
```
Now you can search for methods with `method_containing` and print their models with `print_model`.
You probably want to look at the first or last frame of the trace, to see if the source or sink is present. Then, you will want to follow the frames until you find the problematic method.

### Example

Let's suppose I am investigating a false negative, I want to find in which method we are losing the flow. I could start looking at the last frame, i.e the sink:
```shell
In [2]: method_containing('Landroid/content/Context;.sendOrderedBroadcast')
Out[2]:
['Landroid/content/Context;.sendOrderedBroadcast:(Landroid/content/Intent;Ljava/lang/String;)V',
 'Landroid/content/Context;.sendOrderedBroadcast:(Landroid/content/Intent;Ljava/lang/String;Landroid/content/BroadcastReceiver;Landroid/os/Handler;ILjava/lang/String;Landroid/os/Bundle;)V',
 'Landroid/content/Context;.sendOrderedBroadcastAsUser:(Landroid/content/Intent;Landroid/os/UserHandle;Ljava/lang/String;Landroid/content/BroadcastReceiver;Landroid/os/Handler;ILjava/lang/String;Landroid/os/Bundle;)V']

In [3]: print_model('Landroid/content/Context;.sendOrderedBroadcast:(Landroid/content/Intent;Ljava/lang/String;Landroid/content/BroadcastReceiver;Landroid/os/Handler;ILjava/lang/String;Landroid/os/Bundle;)V')
{
  "method": "Landroid/content/Context;.sendOrderedBroadcast:(Landroid/content/Intent;Ljava/lang/String;Landroid/content/BroadcastReceiver;Landroid/os/Handler;ILjava/lang/String;Landroid/os/Bundle;)V",
  "modes": [
    "skip-analysis",
    "add-via-obscure-feature",
    "taint-in-taint-out",
    "taint-in-taint-this",
    "no-join-virtual-overrides"
  ],
  "position": {
    "path": "android/content/Context.java"
  },
  ...
  "sinks": [
    {
      "callee_port": "Leaf",
      "caller_port": "Argument(1)",
      "kind": "LaunchingComponent",
      "origins": [
        "Landroid/content/Context;.sendOrderedBroadcast:(Landroid/content/Intent;Ljava/lang/String;Landroid/content/BroadcastReceiver;Landroid/os/Handler;ILjava/lang/String;Landroid/os/Bundle;)V"
      ]
    }
  ]
}
```
As expected, the method has a sink on Argument(1), so we are good for now. Next, I want to check the previous frame, which calls `Context.sendOrderedBroadcast`:
```shell
In [2]: method_containing('ShortcutManagerCompat;.requestPinShortcut:')
Out[2]: ['Landroidx/core/content/pm/ShortcutManagerCompat;.requestPinShortcut:(Landroid/content/Context;Landroidx/core/content/pm/ShortcutInfoCompat;Landroid/content/IntentSender;)Z']

In [3]: print_model('Landroidx/core/content/pm/ShortcutManagerCompat;.requestPinShortcut:(Landroid/content/Context;Landroidx/core/content/pm/ShortcutInfoCompat;Landroid/content/IntentSender;)Z')
{
  "method": "Landroidx/core/content/pm/ShortcutManagerCompat;.requestPinShortcut:(Landroid/content/Context;Landroidx/core/content/pm/ShortcutInfoCompat;Landroid/content/IntentSender;)Z",
  "position": {
    "line": 112,
    "path": "androidx/core/content/pm/ShortcutManagerCompat.java"
  },
  ...
  "sinks": [
     ...
    {
      "always_features": [
        "via-obscure",
        "via-obscure-taint-in-taint-this",
        "via-intent-extra",
        "has-intent-extras"
      ],
      "call_position": {
        "line": 130,
        "path": "androidx/core/content/pm/ShortcutManagerCompat.java"
      },
      "callee": "Landroid/content/Context;.sendOrderedBroadcast:(Landroid/content/Intent;Ljava/lang/String;Landroid/content/BroadcastReceiver;Landroid/os/Handler;ILjava/lang/String;Landroid/os/Bundle;)V",
      "callee_port": "Argument(1)",
      "caller_port": "Argument(1).mIntents",
      "distance": 1,
      "kind": "LaunchingComponent",
      "local_positions": [
        {
          "line": 121
        }
      ],
      "origins": [
        "Landroid/content/Context;.sendOrderedBroadcast:(Landroid/content/Intent;Ljava/lang/String;Landroid/content/BroadcastReceiver;Landroid/os/Handler;ILjava/lang/String;Landroid/os/Bundle;)V"
      ]
    }
  ]
}
```
I can see the frame from `ShortcutManagerCompat.requestPinShortcut` on `Argument(1).mIntents` to `Context.sendOrderedBroadcast` on `Argument(1)`. I can keep following frames until I find the method that misses a source or sink.

For frames from the source to the root callable, I should look at `generations`, and for frames from the root callable to the sink, I should look at `sinks`. On the root callable, I should look at `issues`.

As you can see above, methods can have very long signatures. Fortunately, the bento script is also a python REPL, so you can assign them to variables

```shell
In [4]:requestPinShortcut = 'Landroidx/core/content/pm/ShortcutManagerCompat;.requestPinShortcut:(Landroid/content/Context;Landroidx/core/content/pm/ShortcutInfoCompat;Landroid/content/IntentSender;)Z'
In [5]:pm = print_model
In [6]:pm(requestPinShortcut)
{
  "method": "Landroidx/core/content/pm/ShortcutManagerCompat;.requestPinShortcut:(Landroid/content/Context;Landroidx/core/content/pm/ShortcutInfoCompat;Landroid/content/IntentSender;)Z",
  "position": {
    "line": 112,
    "path": "androidx/core/content/pm/ShortcutManagerCompat.java"
  },
  ...
}
```

## Investigating the transfer function

Once you know in which method you are losing the flow or introducing an invalid flow, you will need to run the analysis with logging enabled for that method, using:

<OssOnly>

```shell
mariana-trench \
  --apk-path='your-apk' \
  --log-method='method-name'
```

</OssOnly>
<FbInternalOnly>

```shell
buck run //fbandroid/native/mariana-trench/shim:shim -- \
  --apk-path='your-apk' \
  --log-method='method-name'
```

</FbInternalOnly>

This will log everything the transfer function does in that method, which might be a lot of logs. You can pipe this into a file or into `less`. Using logs, you should be able to see in which instruction you are losing the taint. Remember, the analysis computes a fixpoint, so the method will be analyzed multiple times. You should look at the last time it was analyzed (i.e, end of the logs).

Happy debugging!


---
id: feature-descriptions
title: Feature Glossary
sidebar_label: Feature Glossary
---

As explained in the [features section of the models wiki](../models/#features), a feature can be used to tag a flow and help filtering issues. A feature describes a property of a flow. A feature can be any arbitrary string. A feature that's prefixed with `always-` signals that every path in the issue has that feature associated with it, while lacking that prefix means that at least one path, but not all paths, contains that feature.

This page will cover the purpose of the pre-configured features to help you understand how you can use them best.

## Pre-configured features

- via-caller-exported
  - This feature is applied when the root callable is directly or indirectly called from an exported component defined in the Android manifest. For example, if the root callable is in the `MainActivity` and the `MainActivity` is exported, this feature will be attached. It is needed in order to determine if an `Intent` source is third-party controllable or not. This feature is sometimes accompanied by `via-class` which tells you which class Mariana Trench used to determine that the root callable is called from an exported class.
- via-caller-unexported
  - Same as `via-caller-exported` but applied if the root callable is considered to be called only via unexported components
- via-caller-permission
  - Similair to `via-caller-exported` but applied if the root callable paths to a manifest entry that has a protectionLevel or Android permission declared.
- via-explicit-intent
  - Applied when the taint flow goes via a class or package name setter on an Intent. This can be used to infer whether a launched Intent can resolve to third party apps or only to a specifically defined app (implicit versus explicit intents).
- via-inner-class-this
  - Anonymous classes in Java byte code transfer the taint from the parent class to the anonymous class via `this.this$0` which can lead to [broaden false positives](../models/#taint-broadening). This feature can be used to filter out such flows when they are a common false positive pattern.
- cast:[...]
  - Cast features such as `cast:boolean` are applied when the tainted data is converted to that specific type. This allows for example to filter out data flows such as `taintedString.length()` where the returned tainted integer may no longer be of interest.
- via-obscure
  - Obscure methods are methods for which Mariana Trench doesn't have any byte code available. Therefore we generally apply taint-in-taint-out behaviour on these methods and add the feature `via-obscure` to tell the user that the data flow went along an obscure method.
- via-[...]-broadening
  - Is applied when any of the four broaden operations is applied (see [Models](../models/#taint-broadening)).


---
id: getting-started
title: Getting Started
sidebar_label: Getting Started
---
import useBaseUrl from '@docusaurus/useBaseUrl';

This guide will walk you through setting up Mariana Trench on your machine and get you to find your first remote code execution vulnerability in a small sample app.

## Prerequisites
Mariana Trench requires a recent version of [Python](https://www.python.org/downloads/). On MacOS you can get a current version through [homebrew](https://brew.sh/):

```shell
$ brew install python3
```

On a Debian flavored Linux (Ubuntu, Mint, Debian), you can use `apt-get`:

```shell
$ sudo apt-get install python3 python3-pip python3-venv
```

This guide also assumes you have the [Android SDK](https://developer.android.com/studio) installed and an environment variable `$ANDROID_SDK` pointed to the location of the SDK.

For the rest of this guide, we assume that you are working inside of a [virtual environment](https://docs.python.org/3/tutorial/venv.html). You can set this up with

```shell
$ python3 -m venv ~/.venvs/mariana-trench
$ source ~/.venvs/mariana-trench/bin/activate
(mariana-trench)$
```

The name of the virtual environment in front of your shell prompt indicates that the virtual environment is active.

## Installing Mariana Trench
Inside your virtual environment installing Mariana Trench is as easy as running

```shell
(mariana-trench)$ pip install mariana-trench
```

## Running Mariana Trench
We'll use a small app that is part of our documentation. You can get it by running

```shell
(mariana-trench)$ git clone https://github.com/facebook/mariana-trench
(mariana-trench)$ cd mariana-trench/documentation/sample-app
```

We are now ready to run the analysis

```shell
(mariana-trench)$ mariana-trench \
  --system-jar-configuration-path=$ANDROID_SDK/platforms/android-30/android.jar \
  --apk-path=app/build/outputs/apk/debug/app-debug.apk \
  --source-root-directory=app/src/main/java
# ...
INFO Analyzed 68886 models in 4.04s. Found 4 issues!
# ...
```

The analysis has found 4 issues in our sample app. The output of the analysis is a set of specifications for each method of the application.

## Post Processing
The specifications themselves are not meant to be read by humans. We need an additional processing step in order to make the results more presentable. We do this with [SAPP](https://github.com/facebook/sapp) PyPi installed for us:

```shell
(mariana-trench)$ sapp --tool=mariana-trench analyze .
(mariana-trench)$ sapp --database-name=sapp.db server --source-directory=app/src/main/java
# ...
2021-05-12 12:27:22,867 [INFO]  * Running on http://localhost:13337/ (Press CTRL+C to quit)
```

The last line of the output tells us that SAPP started a local webserver that lets us look at the results. Open the link and you will see the 4 issues found by the analysis.

## Exploring Results
Let's focus on the remote code execution issue found in the sample app. You can identify it by its issue code `1` (for all remote code executions) and the callable `void MainActivity.onCreate(Bundle)`. With only 4 issues to see it's easy to identify the issue manually but once more rules run, the filter functionality at the top right of the page comes in handy.

<img alt="Single Issue Display" src={useBaseUrl('img/issue.png')} />

The issue tells you that Mariana Trench found a remote code execution in `MainActivity.onCreate` where the data is coming from `Activity.getIntent` one call away, and flows into the constructor of `ProcessBuilder` 3 calls away. Click on "Traces" in the top right corner of the issue to see an example trace.

The trace surfaced by Mariana Trench consists of three parts.

The *source trace* represents where the data is coming from. In our example, the trace is very short: `Activity.getIntent` is called in `MainActivity.onCreate` directly.
<img alt="Trace Source" src={useBaseUrl('img/trace_source.png')} />

The *trace root* represents where the source trace meets the sink trace. In our example this is the `MainActivity.onCreate` method.
<img alt="Trace Root" src={useBaseUrl('img/trace_root.png')} />

The final part of the trace is the *sink trace*: This is where the data from the source flows down into a sink. In our example from `onCreate`, to `onClick`, to `execute`, and finally into the constructor of `ProcessBuilder`.
<img alt="Trace Source" src={useBaseUrl('img/trace_sink.png')} />

## Configuring Mariana Trench
You might be asking yourself, "how does the tool know what is user controlled data, and what is a sink?". This guide is meant to quickly get you started on a small app. We did not cover how to configure Mariana Trench. You can read more about that in the [Configuration section](./configuration.md).


---
id: known-false-negatives
title: Known False Negatives
sidebar_label: Known False Negatives
---
import {OssOnly, FbInternalOnly} from 'docusaurus-plugin-internaldocs-fb/internal';
import FbKnownFalseNegatives from './fb/known_false_negatives.md';

Like any static analysis tools, Mariana Trench has false negatives. This documents the more well-known places where taint is dropped. Note that this is not an exhaustive list. See [this wiki](./debugging_fp_fns.md) for instructions on how to debug them.

Many of these options are *configurable*, not hard limits. There are analysis time, memory, and quality tradeoffs.

## Trace too Long

Mariana Trench stops propagating taint beyond a certain depth. This depth is currently configured at 7. In code:
```
// This method has depth 1.
public int get_source_1() { return source(); }

// This method has depth 2.
public int get_source_2() { return get_source_1(); }

...

// This method has depth 7.
public int get_source_7() { return get_source_6(); }

// This method theoretically has depth 8, but MT drops the source here.
public int get_source_8() { return get_source_7(); }
```
**Workaround:** If the chain of wrappers obviously leads to a source or sink, instead of defining the source at `source()`, one could write an additional model marking `get_source_7()` as a source.

## Fields of Fields of Fields of Fields...

Taint of an object is dropped when it occurs too deep within the object. This depth is configured at 4. In code:
```
public void taintedThis() {
  this.mField1 = source(); // This is OK
  this.mField1.mField2.mField3.mField4.mField5 = source(); // This gets dropped
}
```

**Workaround:** This isn’t much of a workaround, but one can manually configure the source on “this.mField1.....mField4” instead. This will be a form of over-abstraction and could lead to false positives.

## Fanouts

If a virtual method has too many overrides, beyond a certain number (currently configured at 40), we stop considering all overrides and look only at the direct method being called. In code:
```
interface IFace {
  public int possibleSource();
}

class Class1 implements IFace {
  public int possibleSource() { return 1; }
}
...

class Class41 implements IFace {
  public int possibleSource() { return source(); }
}

int maybeIssue(IFace iface) {
  // The source will get dropped here because there are too many overrides.
  // MT will not report an issue.
  sink(iface.possibleSource());
}


```
**Workaround:** Unfortunately, there are no known workarounds.

## Propagation across Arguments

Mariana Trench computes propagations for each method (this may be known as “tito” (taint-in-taint-out) in other tools). Propagations tell the analysis that if an argument is tainted by a source, whether its return value, or the method’s “this” object become tainted by the argument. However, without explictly specifying `--propagate-across-arguments`, Mariana Trench does not propagate taint from one argument to another. In code:
```
void setIntentValue(Intent intent, Uri uri) {
  // MT sees that intent.putExtra has a propagation from uri (Argument(2)) to
  // intent (Argument(0) or this).
  intent.putExtra("label", uri);

  // However, when it finishes analyzing setIntentValue, it will not track the
  // propagation from uri to intent.
}

void falseNegative() {
  Uri uri = source();
  Intent intent = new Intent();

  // If this were the code, MT will detect a source->sink flow at launchActivitySink.
  // intent.putExtra("label", uri);

  // MT loses the flow from uri->intent at this point.
  setIntentValue(intent, uri);

  launchActivitySink(intent);
}
```
**Workaround 1:** Write an explicit propagation model for the method. While Mariana Trench does not infer propagations across arguments, it does allow manual specification of such models.

**Workaround 2:** Enable `--propagate-across-arguments`, which enables taint propagation across method invocations for object. Note that the behaviour is enabled globally, meaning that this may incur a significant runtime and memory overhead.

<FbInternalOnly> <FbKnownFalseNegatives/> </FbInternalOnly>


---
id: models
title: Models & Model Generators
sidebar_label: Models & Model Generators
---

import FbModels from './fb/models.md';

The main way to configure the analysis is through defining model generators. Each model generator defines (1) a **filter**, made up of constraints to specify the methods (or fields) for which a model should be generated, and (2) a **model**, an abstract representation of how data flows through a method.

Model generators are what define Sink and Source kinds which are the key component of [Rules](/rules.md). Model generators can do other things too, like attach **features** (a.k.a. breadcrumbs) to flows and **sanitize** (redact) flows which go through certain "data-safe" methods (e.g. a method which hashes a user's password).

Filters are conceptually straightforward. Thus, this page focuses heavily on conceptualizing and providing examples for the various types of models. See the [Model Generators](#model-generators) section for full implementation documentation for both filters and models.

## Models

A model is an abstract representation of how data flows through a method.

A model essentialy consists of:

- [Sources](#sources): a set of sources that the method produces or receives on parameters;
- [Sinks](#sinks): a set of sinks on the method;
- [Propagation](#propagation): a description of how the method propagates taint coming into it (e.g, the first parameter updates the second, the second parameter updates the return value, etc.);
- [Attach to Sources](#attach-to-sources): a set of features/breadcrumbs to add on an any sources flowing out of the method;
- [Attach to Sinks](#attach-to-sinks): a set of features/breadcrumbs to add on sinks of a given parameter;
- [Attach to Propagations](#attach-to-propagations): a set of features/breadcrumbs to add on propagations for a given parameter or return value;
- [Add Features to Arguments](#add-features-to-arguments): a set of features/breadcrumbs to add on any taint that might flow in a given parameter;
- [Sanitizers](#sanitizers): specifications of taint flows to stop;
- [Modes](#modes): a set of flags describing specific behaviors (see below).

Models can be specified in JSON. For example to mark the string parameter to our `Logger.log` function as a sink we can specify it as

```json
{
  "find": "methods",
  "where": [
    {
      "constraint": "signature_match",
      "parent": "Lcom/example/Logger;",
      "name": "log"
    }
  ],
  "model": {
    "sinks": [
      {
        "kind": "Logging",
        "port": "Argument(1)"
      }
    ]
  }
}
```

Note that the naming of methods follow the [Dalvik's bytecode format](#method-name-format).

### Method name format

The format used for method names is:

`<className>.<methodName>:(<parameterType1><parameterType2>)<returnType>`

Example: `Landroidx/fragment/app/Fragment;.startActivity:(Landroid/content/Intent;)V`

For the parameters and return types use the following table to pick the correct one (please refer to [JVM doc](https://docs.oracle.com/javase/specs/jvms/se7/html/jvms-4.html#jvms-4.3.2-200) for more details)

- V - void
- Z - boolean
- B - byte
- S - short
- C - char
- I - int
- J - long (64 bits)
- F - float
- D - double (64 bits)

Classes take the form `Lpackage/name/ClassName;` - where the leading `L` indicates that it is a class type, `package/name/` is the package that the class is in. A nested class will take the form `Lpackage/name/ClassName$NestedClassName` (the `$` will need to be double escaped `\\$` in json regex).

> **NOTE 1:** Instance (i.e, non-static) method parameters are indexed starting from 1! The 0th parameter is the `this` parameter in dalvik byte-code. For static method parameters, indices start from 0.

> **NOTE 2:** In a constructor (\<init\> method), parameters are also indexed starting from 1. The 0th parameter refers to the instance being constructed, similar to the `this` reference.

### Access path format

An access path describes the symbolic location of a taint. This is commonly used to indicate where a source or a sink originates from. The "port" field of any model is represented by an access path.

An access path is composed of a root and a path.

The root is either:

- `Return`, representing the returned value;
- `Argument(x)` (where `x` is an integer), representing the parameter number `x`;

The path is a (possibly empty) list of path elements. A path element can be any of the following kinds:

- `field`: represents a field name. String encoding is a dot followed by the field name: `.field_name`;
- `index`: represents a user defined index for dictionary like objects. String encoding uses square braces to enclose any user defined index: `[index_name]`;
- `any index`: represents any or unresolved indices in dictionary like objects. String encoding is an asterisk enclosed in square braces: `[*]`;
- `index from value of`: captures the value of the specified callable's port seen at its callsites during taint flow analysis as an `index` or `any index` (if the value cannot be resolved). String encoding uses _argument root_ to specify the callable's port and encloses it in `[<`...`>]` to represent that its value is resolved at the callsite to create an index: `[<Argument(x)>]`;

Examples:

- `Argument(1).name` corresponds to the _field_ `name` of the second parameter;
- `Argument(1)[name]` corresponds to the _index_ `name` of the dictionary like second parameter;
- `Argument(1)[*]` corresponds to _any index_ of the dictionary like second parameter;
- `Argument(1)[<Argument(2)>]` corresponds to an _index_ of the dictionary like second parameter whose value is resolved from the third parameter;
- `Return` corresponds to the returned value;
- `Return.x` corresponds to the field `x` of the returned value;

### Kinds

A source has a **kind** that describes its content (e.g, user input, file system, etc). A sink also has a **kind** that describes the operation the method performs (e.g, execute a command, read a file, etc.). Kinds can be arbitrary strings (e.g, `UserInput`). We usually avoid whitespaces.

### Sources

Sources describe taint *produced* or *received* by a given method. A source has a **kind** that describes its content (e.g, user input, file system, etc).
- A method *produces* a source kind if invoking the method implies the source kind *flows out* from it. The source kind can flow out via the return value or through a parameter (pass by reference semantics).
- A method *receives* a source kind if a source kind is always assumed to *flow in* via an argument regardless of the method's callsite.

Here is an example where the source *flows out* through the return value:

```java
public static String getPath() {
    return System.getenv().get("PATH");
}
```

The JSON model generator for this method could be:

```json
{
  "find": "methods",
  "where": [
    {
      "constraint": "signature_match",
      "parent": "Lcom/example/Class;",
      "name": "getPath"
    }
  ],
  "model": {
    "sources": [
      {
        "kind": "UserControlled",
        "port": "Return"
      }
    ]
  }
}
```

Here is an example where the source *flows in* via an argument:

```java
class MyActivity extends Activity {
  public void onNewIntent(Intent intent) {
    // intent should be considered a source here.
  }
}
```

The JSON model generator for this method could be:

```json
{
  "find": "methods",
  "where": [
    {
      "constraint": "signature_match",
      "extends": "Landroid/app/Activity",
      "name": "onNewIntent"
    }
  ],
  "model": {
    "sources": [
      {
        "kind": "UserControlled",
        "port": "Argument(1)"
      }
    ]
  }
}
```

Here is an example where source *flows out* via an argument:
```java
public static void updateIntent(Intent intent) {}

void createAndUseIntent() {
  MyIntent myIntent = new MyIntent();
  // myIntent is not a source. This is safe.
  sink(myIntent);

  updateIntent(myIntent);
  // myIntent is now a source. This is now a flow.
  sink(myIntent);
}
```

The JSON model generator for this method could be:

```json
{
  "find": "methods",
  "where": [
    {
     "constraint": "signature_match",
      "parent": "Lcom/example/Class;",
      "name": "updateIntent"
    }
  ],
  "model": {
    "generations": [
      {
        "kind": "UserControlled",
        "port": "Argument(0)"
      }
    ]
  }
}
```

Note on the use of "generations" vs "sources": "generations" indicates that the source kind is *produced* and *flows out* via the specified port. When the port is "Return", "generations" and "sources" are equivalent.

"generations" are also useful to mark the `this` reference of an instance as sources. Instances are created using constructors, which are special `<init>` methods with return type void. But, as mentioned in Note 2 above, constructors create a special 0th parameter to refer to the instance being constructed (i.e. `this`). Here is an example where a constructor marks the instance as a source:
```java
class SourceIntent extends Intent {
  SourceIntent() {}
}

void createAndUseIntent() {
  SourceIntent sourceIntent = new SourceIntent();
  // sourceIntent is a source.
  sink(myIntent);
}
```

The JSON model generator for the constructor method could be:

```json
{
  "find": "methods",
  "where": [
    {
     "constraint": "signature_match",
      "parent": "Lcom/example/SourceIntent;",
      "name": "<init>"
    }
  ],
  "model": {
    "generations": [
      {
        "kind": "UserControlled",
        "port": "Argument(0)"
      }
    ]
  }
}
```




### Sinks

Sinks describe dangerous or sensitive methods in the code. A sink has a **kind** that represents the type of operation the method does (e.g, command execution, file system operation, etc). A sink must be attached to a given parameter of the method. A method can have multiple sinks.

Here is an example of a sink:

```java
public static String readFile(String path, String extension, int mode) {
    // Return the content of the file path.extension
}
```

Since `path` and `extension` can be used to read arbitrary files, we consider them sinks. We do not consider `mode` as a sink since we do not care whether the user can control it. The JSON model generator for this method could be:

```json
{
  "find": "methods",
  "where": [
    {
      "constraint": "signature_match",
      "parent": "Lcom/example/Class",
      "name": "readFile"
    }
  ],
  "model": {
    "sinks": [
      {
        "kind": "FileRead",
        "port": "Argument(0)"
      },
      {
        "kind": "FileRead",
        "port": "Argument(1)"
      }
    ]
  }
}
```

### Return Sinks

Return sinks can be used to describe that a method should not return tainted information. A return sink is just a normal sink with a `Return` port.

### Propagation

Propagations − also called **tito** (Taint In Taint Out) or **passthrough** in other tools − describe how the method propagates taint. A propagation as an **input** (where the taint comes from) and an **output** (where the taint is moved to).

Here is an example of a propagation:

```java
public static String concat(String x, String y) {
  return x + y;
}
```

The return value of the method can be controlled by both parameters, hence it has the propagations `Argument(0) -> Return` and `Argument(1) -> Return`. The JSON model generator for this method could be:

```json
{
  "find": "methods",
  "where": [
    {
      "constraint": "signature_match",
      "parent": "Lcom/example/Class",
      "name": "concat"
    }
  ],
  "model": {
    "propagation": [
      {
        "input": "Argument(0)",
        "output": "Return"
      },
      {
        "input": "Argument(1)",
        "output": "Return"
      }
    ]
  }
}
```

#### Propagation with Transforms

Propagations can additionally specify a list of "transforms". This is an ordered list of *transform kinds* which specifies the transformations that are applied to the input of the propagation. Transform kinds can be used to specify methods that flows must pass through to be valid flows. Transform kinds, like source and sink kinds, must be included as a part of the [rule](./rules.md#transforms) to add the transform constraint.


```json
"propagation": [
  {
    "input": "Argument(0)",
    "output": "Return",
    "transforms": [
      "IntentData"
    ]
  }
]
```


### Features

Features (also called **breadcrumbs**) can be used to tag a flow and help filtering issues. A feature describes a property of a flow. A feature can be any arbitrary string.

For instance, the feature `via-numerical-operator` is used to describe that the data flows through a numerical operator such as an addition.

Features are very useful to filter flows in the SAPP UI. E.g. flows with a cast from string to integer are can sometimes be less important during triaging since controlling an integer is more difficult to exploit than controlling a full string.

Note that features **do not stop** the flow, they just help triaging.

#### Attach to Sources

_Attach to sources_ is used to add a set of [features](#features) on any sources flowing out of a method through a given parameter or return value.

For instance, if we want to add the feature `via-signed` to all sources flowing out of the given method:

```java
public String getSignedCookie();
```

We could use the following JSON model generator:

```json
{
  "find": "methods",
  "where": [
    {
      "constraint": "signature_match",
      "parent": "Lcom/example/Class",
      "name": "getSignedCookie"
    }
  ],
  "model": {
    "attach_to_sources": [
      {
        "features": [
          "via-signed"
        ],
        "port": "Return"
      }
    ]
  }
}
```

Note that this is only useful for sources inferred by the analysis. If you know that `getSignedCookie` returns a source of a given kind, you should use a source instead.

#### Attach to Sinks

_Attach to sinks_ is used to add a set of [features](#features) on all sinks on the given parameter of a method.

For instance, if we want to add the feature `via-user` on all sinks of the given method:

```java
class User {
  public static User findUser(String username) {
    // The code here might use SQL, Thrift, or anything. We don't need to know.
  }
}
```

We could use the following JSON model generator:

```json
{
  "find": "methods",
  "where": [
    {
      "constraint": "signature_match",
      "parent": "Lcom/example/User",
      "name": "findUser"
    }
  ],
  "model": {
    "attach_to_sinks": [
      {
        "features": [
          "via-user"
        ],
        "port": "Argument(0)"
      }
    ]
  }
}
```

Note that this is only useful for sinks inferred by the analysis. If you know that `findUser` is a sink of a given kind, you should use a sink instead.

#### Attach to Propagations

_Attach to propagations_ is used to add a set of [features](#features) on all propagations from or to a given parameter or return value of a method.

For instance, if we want to add the feature `via-concat` to the propagations of the given method:

```java
public static String concat(String x, String y);
```

We could use the following JSON model generator:

```json
{
  "find": "methods",
  "where": [
    {
      "constraint": "signature_match",
      "parent": "Lcom/example/Class",
      "name": "concat"
    }
  ],
  "model": {
    "attach_to_propagations": [
      {
        "features": [
          "via-concat"
        ],
        "port": "Return" // We could also use Argument(0) and Argument(1)
      }
    ]
  }
}
```

Note that this is only useful for propagations inferred by the analysis. If you know that `concat` has a propagation, you should model it as a propagation directly.

#### Add Features to Arguments

_Add features to arguments_ is used to add a set of [features](#features) on all sources that **might** flow on a given parameter of a method.

_Add features to arguments_ implies _Attach to sources_, _Attach to sinks_ and _Attach to propagations_, but it also accounts for possible side effects at call sites.

For instance:

```java
public static void log(String message) {
  System.out.println(message);
}
public void buyView() {
  String username = getParameter("username");
  String product = getParameter("product");
  log(username);
  buy(username, product);
}
```

Technically, the `log` method doesn't have any source, sink or propagation. We can use _add features to arguments_ to add a feature `was-logged` on the flow from `getParameter("username")` to `buy(username, product)`. We could use the following JSON model generator for the `log` method:

```json
{
  "find": "methods",
  "where": [
    {
      "constraint": "signature_match",
      "parent": "Lcom/example/Class",
      "name": "log"
    }
  ],
  "model": {
    "add_features_to_arguments": [
      {
        "features": [
          "was-logged"
        ],
        "port": "Argument(0)"
      }
    ]
  }
}
```

#### Via-type Features

_Via-type_ features are used to keep track of the type of a callable’s port seen at its callsites during taint flow analysis. They are specified in model generators within the “sources” or “sinks” field of a model with the “via_type_of” field. It is mapped to a nonempty list of ports of the method for which we want to create via-type features.

For example, if we were interested in the specific Activity subclasses with which the method below was called:

```java

public void startActivityForResult(Intent intent, int requestCode);

// At some callsite:
ActivitySubclass activitySubclassInstance;
activitySubclassInstance.startActivityForResult(intent, requestCode);

```

we could use the following JSON to specify a via-type feature that would materialize as `via-type:ActivitySubclass`:

```json
{
  "find": "methods",
  "where": [
    {
      "constraint": "signature_match",
      "extends": "Landroid/app/Activity",
      "name": "startActivityForResult"
    }
  ],
  "model": {
    "sinks": [
      {
        "port": "Argument(1)",
        "kind": "SinkKind",
        "via_type_of": [
          "Argument(0)"
        ]
      }
    ]
  }
}
```

#### Via-value Features

_Via-value_ feature captures the value of the specified callable's port seen at its callsites during taint flow analysis. They are specified similar to `Via-type` features -- in model generators within the "sources", "sinks"  or "add_features_to_arguments" field of a model with the "via_value_of" field. It is mapped to a nonempty list of ports of the method for which we want to create via-value features.

For example, if we were interested in the specific `mode` with which the method below was called:

```java
public void log(String mode, String message);

class Constants {
  public static final String MODE = "M1";
}

// At some callsite:
log(Constants.MODE, "error message");

```

we could use the following JSON to specify a via-value feature that would materialize as `via-value:M1`:

```json
{
  "find": "methods",
  "where": [
    {
      "constraint": "signature_match",
      "parent": "Lcom/example/Class",
      "name": "log"
    }
  ],
  "model": {
    "sinks": [
      {
        "port": "Argument(1)",
        "kind": "SinkKind",
        "via_value_of": [
          "Argument(0)"
        ]
      }
    ]
  }
}
```

Note that this only works for numeric and string literals. In cases where the argument is not a constant, the feature will appear as `via-value:unknown`.

Note: `via_type_of` and `via_value_of` allow specifying a tag, which will be provided in the instantiated breadcrumb. For instance `via-foo-value:bar`, for a tag "foo". This can be used to differentiate from other via-value or via-type breadcrumbs.
```json
"via_type_of": [
  {
    "port": "Argument(1)",
    "tag": "differentiator"
  }
]
```
This would create the feature `via-differentiator-type:Lcom/example/Class`.

For backward compatibility, we allow these to be mixed with normal ports in a list
```json
"via_value_of": [
  "Argument(0)",
  {
    "port": "Argument(1)",
    "tag": "error-mode"
  },
  "Argument(2)"
]
```

#### Annotation Features

In model generators we can also use annotation features, which translate to regular user features based on annotation parameter values. This feature is also compatible with `for_all_parameters`.

Config example:
```json
{
  "model_generators": [
    {
      "find": "methods",
      "where": [
        {
          "constraint": "signature_match",
          "parent": "Lcom/facebook/marianatrench/integrationtests/AnnotationFeature;",
          "name": "getSourceWithMethodAnnotation"
        }
      ],
      "model": {
        "generations": [
          {
            "kind": "Source",
            "port": "Return",
            "via_annotation": [
              {
                "type": "Lcom/facebook/marianatrench/integrationtests/Path;",
                "target": "Return"
              }
            ]
          }
        ]
      }
    },
    {
      "find": "methods",
      "where": [
        {
          "constraint": "signature_match",
          "parent": "Lcom/facebook/marianatrench/integrationtests/AnnotationFeature;",
          "name": "getSourceWithParameterAnnotation"
        }
      ],
      "model": {
        "generations": [
          {
            "kind": "Source",
            "port": "Return",
            "via_annotation": [
              {
                "type": "Lcom/facebook/marianatrench/integrationtests/QueryParam;",
                "target": "Argument(1)"
              },
              {
                "type": "Lcom/facebook/marianatrench/integrationtests/OtherQueryParam;",
                "target": "Argument(2)",
                "tag": "ParameterNameLabel",
                "annotation_parameter": "description"
              }
            ]
          }
        ]
      }
    }
  ]
}
```

Java class with annotations:
```java
public class AnnotationFeature {

  @Path("/issue_1")
  Object getSourceWithMethodAnnotation() {
    return new Object();
  }

  Object getSourceWithParameterAnnotation(@QueryParam("query_param_name") String value, @OtherQueryParam(value = "other_query_param_name", description = "other_query_param_name_description") String description) {
    return "unrelated";
  }

  void testSourceWithMethodAnnotation() {
    Object source = getSourceWithMethodAnnotation();
    Origin.sink(source);
  }

  void testSourceWithParameterAnnotation() {
    Object source = getSourceWithParameterAnnotation("argument_value");
    Origin.sink(source);
  }
}
```

Resulting issues:

```json
{
  "issues" :
  [
    {
      "always_features" :
      [
        "via-annotation:/issue_1"
      ],
      "callee" : "Lcom/facebook/marianatrench/integrationtests/Origin;.sink:(Ljava/lang/Object;)V",
...
{
  "issues" :
  [
    {
      "always_features" :
      [
        "via-ParameterNameLabel-annotation:description_instead_of_value"
      ],
      "callee" : "Lcom/facebook/marianatrench/integrationtests/Origin;.sink:(Ljava/lang/Object;)V",
...
```

### Taint Broadening

**Taint broadening** (also called **collapsing**) happens when Mariana Trench needs to make an approximation about a taint flow. It is the operation of reducing a **taint tree** into a single element. A **taint tree** is a tree where edges are field names and nodes are taint element. This is how Mariana Trench represents internally which fields (or sequence of fields) are tainted.

For instance, analyzing the following code:

```java
MyClass var = new MyClass();
var.a = sourceX();
var.b.c = sourceY();
var.b.d = sourceZ();
```

The taint tree of variable `var` would be:

```
      .
  a /   \ b
 { X }    .
       c / \ d
     { Y }  { Z }
```

After collapsing, the tree is reduced to a single node `{ X, Y, Z }`, which is less precise.

In conclusion, taint broadening effectively leads to considering the whole object as tainted while only some specific fields were initially tainted. This might happen for the correctness of the analysis or for performance reasons.

In the following sections, we will discuss when collapsing can happen. In most cases, a feature is automatically added on collapsed taint to help detect false positives.

#### Propagation Broadening

Taint collapsing is applied when taint is propagated through a method.

For instance:

```java
MyClass input = new MyClass();
input.a = SourceX();
MyClass output = SomeClass.UnknownMethod(input);
Sink(output.b); // Considered an issue since `output` is considered tainted. This could be a False Negative without collapsing.
```

In that case, the [feature](#feature) `via-propagation-broadening` will be automatically added on the taint. This can help identify false positives.

If you know that this method **preserves the structure** of the parameter, you could specify a model and disable collapsing using the `collapse` attribute within a [`propagation`](#propagation):

```json
{
  "find": "methods",
  "where": [
    {
      "constraint": "signature_match",
      "parent": "Lcom/example/SomeClass",
      "name": "UnknownMethod"
    }
  ],
  "model": {
    "propagation": [
      {
        "input": "Argument(0)",
        "output": "Return",
        "collapse": false
      }
    ]
  }
}
```

Note that Mariana Trench can usually infer when a method propagates taint without collapsing it when it has access to the code of that method and subsequent calls. For instance:

```java
public String identity(String x) {
  // Automatically infers a propagation `Arg(0) -> Return` with `collapse=false`
  return x;
}
```

##### Issue Broadening Feature

The `via-issue-broadening` feature is added to issues where the taint flowing into the sink was not held directly on the object passed in but on one of its fields. For example:

```java
Class input = new Class();
input.field = source();
sink(input); // `input` is not tainted, but `input.field` is tainted and creates an issue
```

##### Widen Broadening Feature

For performance reasons, if a given taint tree becomes very large (either in depth or in number of nodes at a given level), Mariana Trench collapses the tree to a smaller size. In these cases, the `via-widen-broadening` feature is added to the collapsed taint

```java
Class input = new Class();
if (\* condition *\) {
  input.field1 = source();
  input.field2 = source();
  ...
} else {
  input.fieldA = source();
  input.fieldB = source();
  ...
}
sink(input); // Too many fields are sources so the whole input object becomes tainted
```

### Sanitizers

Specifying sanitizers on a model allow us to stop taint flowing through that method. In Mariana Trench, they can be one of three types -

- `sources`: prevent any taint sources from flowing out of the method
- `sinks`: prevent taint from reaching any sinks within the method
- `propagations`: prevent propagations from being inferred between any two ports of the method.

These can be specified in model generators as follows -

```json
{
  "find": "methods",
  "where": ...,
  "model": {
    "sanitizers": [
      {
        "sanitize": "sources"
      },
      {
        "sanitize": "sinks"
      },
      {
        "sanitize": "propagations"
      }
    ],
    ...
  }
}
```

Note, if there are any user-specified sources, sinks or propagations on the model, sanitizers will not affect them, but it will prevent them from being propagated outward to callsites.

#### Kind-specific Sanitizers

`sources` and `sinks` sanitizers may include a list of kinds (each with or without a partial_label) to restrict the sanitizer to only sanitizing taint of those kinds. (When unspecified, as in the example above, all taint is sanitized regardless of kind).

```json
"sanitizers": [
  {
    "sanitize": "sinks",
    "kinds": [
      {
        "kind": "SinkKindA"
      },
      {
        "kind": "SinkKindB",
        "partial_label": "A"
      }
    ]
  }
]
```

#### Port-specific Sanitizers

Sanitizers can also specify a specific port ([access path](models.md#access-path-format) root) they sanitize (ignoring all the rest). This field `port` has a slightly different meaning for each kind of sanitizer -

- `sources`: represents the output port through which sources may not leave the method
- `sinks`: represents the input port through which taint may not trigger any sinks within the model
- `propagations`: represents the input port through which a propagation to any other port may not be inferred

For example if the following method

```java
public void someMethod(Object argument1, Object argument2) {
  toSink(argument1);
  toSink(argument2);
}
```

had the following sanitizer in its model,

```json
"sanitizers": [
  {
    "sanitize": "sinks",
    "port": "Argument(1)"
  }
]
```

Then a source flowing into `argument1` would be able to cause an issue, but not a source flowing into `argument2`.

Kind and port specifications may be included in the same sanitizer.

### Modes

Modes are used to describe specific behaviors of methods. Available modes are:

- `skip-analysis`: skip the analysis of the method;
- `add-via-obscure-feature`: add a feature/breadcrumb called `via-obscure:<method>` to sources flowing through this method;
- `taint-in-taint-out`: propagate the taint on arguments to the return value;
- `taint-in-taint-this`: propagate the taint on arguments into the `this` parameter;
- `no-join-virtual-overrides`: do not consider all possible overrides when handling a virtual call to this method;
- `no-collapse-on-propagation`: do not collapse input paths when applying propagations;
- `alias-memory-location-on-invoke`: aliases existing memory location at the callsite instead of creating a new one;
- `strong-write-on-propagation`: performs a strong write from input path to the output path on propagation;

### Default model

A default model is created for each method, except if it is provided by a model generator. The default model has a set of heuristics:

If the method has no source code, the model is automatically marked with the modes `skip-analysis` and `add-via-obscure-feature`.

If the method has more than 40 overrides, it is marked with the mode `no-join-virtual-overrides`.

Otherwise, the default model is empty (no sources/sinks/propagations).

### Field Models

These models represent user-defined taint on class fields (as opposed to methods, as described in all the previous sections on this page). They are specified in a similar way to method models as described below.

> **NOTE:** Field sources should not be applied to fields that are both final and of a primitive type (`int`, `char`, `float`, etc as well as `java.lang.String`) as the Java compiler optimizes accesses of these fields in the bytecode into accesses of the constant value they hold. In this scenario, Mariana Trench has no way of recognizing that the constant was meant to carry a source.

Example field model generator for sources:

```json
{
  "find": "fields",
  "where": [
    {
      "constraint": "name",
      "pattern": "SOURCE_EXAMPLE"
    }
  ],
  "model": {
    "sources" : [
      {
        "kind": "FieldSource"
      }
    ]
  }
}
```

Example code:

```java
public class TestClass {
  // Field that we know to be tainted
  public Object SOURCE_EXAMPLE = ...;

  void flow() {
    sink(EXAMPLE, ...);
  }
}
```

Example field model generator for sinks:

```json
{
  "find": "fields",
  "where": [
    {
      "constraint": "name",
      "pattern": "SINK_EXAMPLE"
    }
  ],
  "model": {
    "sinks" : [
      {
        "kind": "FieldSink"
      }
    ]
  }
}
```

Example code:

```java
public class TestClass {
  public Object SINK_EXAMPLE = ...;

  void flow() {
    SINK_EXAMPLE = source();
  }
}
```

Field signature formats follow the Dalvik bytecode format similar to methods as discussed [above](#method-name-format). This is of the form `<className>.<fieldName>:<fieldType>`.

### Literal Models

Literal models represent user-defined taints on string literals matching configurable regular expressions. They can only be configured as sources and are intended to identify suspicious patterns, such as user-controlled data being concatenated with a string literal which looks like an SQL query.

> **NOTE:** Each use of a literal in the analysed code which matches a pattern in a literal model will generate a new taint which needs to be explored by Mariana Trench. Using overly broad patterns like `.*` should thus be avoided, as they can lead to poor performance and high memory usage.

Example literal models:

```
[
  {
    "pattern": "SELECT \\*.*",
    "description": "Potential SQL Query",
    "sources": [
      {
        "kind": "SqlQuery"
      }
    ]
  },
  {
    "pattern": "AI[0-9A-Z]{16}",
    "description": "Suspected Google API Key",
    "sources": [
      {
        "kind": "GoogleAPIKey"
      }
    ]
  }
]
```

Example code:

```java
void testRegexSource() {
  String prefix = "SELECT * FROM USERS WHERE id = ";
  String aci = getAttackerControlledInput();
  String query = prefix + aci; // Sink
}

void testRegexSourceGoogleApiKey() {
  String secret = "AIABCD1234EFGH5678";
  sink(secret);
}
```

## Model Generators

Mariana Trench allows for dynamic model specifications. This allows a user to specify models of methods before running the analysis. This is used to specify sources, sinks, propagation and modes.

The model generator files must have the extension `.models`. The locations to search for these files must be provided using the `--model-generator-search-paths` argument.

Model generators to use during analysis are listed in a *model generator configuration file* and specified using the `--model-generator-configuration-paths` argument. By default, we use [`default_generator_config.json`](https://github.com/facebook/mariana-trench/blob/main/configuration/default_generator_config.json). Any other `.models` files found in the search paths but not listed in the configuration file are ignored.

### Example

Examples of model generators are located in the [`configuration/model-generators`](https://github.com/facebook/mariana-trench/tree/main/configuration/model-generators) directory.

Below is an example of a JSON model generator:

```json
{
  "model_generators": [
    {
      "find": "methods",
      "where": [{"constraint": "name", "pattern": "toString"}],
      "model": {
        "propagation": [
          {
            "input": "Argument(0)",
            "output": "Return"
          }
        ]
      }
    },
    {
      "find": "methods",
      "where": [
        {
          "constraint": "parent",
          "inner": {
            "constraint": "extends",
            "inner": {
              "constraint": "name",
              "pattern": "SandcastleCommand"
            }
          }
        },
        {"constraint": "name", "pattern": "Time"}
      ],
      "model": {
        "sources": [
          {
            "kind": "Source",
            "port": "Return"
          }
        ]
      }
    },
    {
      "find": "methods",
      "where": [
        {
          "constraint": "parent",
          "inner": {
            "constraint": "extends",
            "inner": {"constraint": "name", "pattern": "IEntWithPurposePolicy"}
          }
        },
        {"constraint": "name", "pattern": "gen.*"},
        {
          "constraint": "parameter",
          "idx": 0,
          "inner": {
            "constraint": "type",
            "kind": "extends",
            "class": "IViewerContext"
          }
        },
        {
          "constraint": "return",
          "inner": {
            "constraint": "extends",
            "inner": {"constraint": "name", "pattern": "Ent"}
          }
        }
      ],
      "model": {
        "modes": ["add-via-obscure-feature"],
        "sinks": [
          {
            "kind": "Sink",
            "port": "Argument(0)",
            "features": ["via-gen"]
          }
        ]
      }
    }
  ]
}
```

### Specification

Each JSON file is a JSON object with a key `model_generators` associated with a list of "rules".

Each "rule" defines a "filter" (which uses "constraints" to specify methods for which a "model" should be generated) and a "model". A rule has the following key/values:

- `find`: The type of thing to find. We support `methods` and `fields`;
- `where`: A list of "constraints". All constraints **must be satisfied** by a method or field in order to generate a model for it. All the constraints are listed below, grouped by the type of object they are applied to:

  - **Method**:

    - `signature_match`: Expects at least one of the two allowed groups of extra properties: `[name | names] [parent | parents | extends [include_self]]` where:
      - `name` (a single string) or `names` (a list of alternative strings): is exact matched to the method name
      - `parent` (a single string) or `parents` (a list of alternative strings) is exact matched to the class of the method or `extends` (either a single string or a list of alternative strings) is exact matched to the base classes or interfaces of the method. `extends` allows an optional property `include_self` which is a boolean to indicate if the constraint is applied to the class itself or not (defaults to `true`).
    - `signature | signature_pattern`: Expects an extra property `pattern` which is a regex (with appropriate escaping) to fully match the full signature (class, method, argument types) of a method;
      - **NOTE:** Usage of this constraint is discouraged as it has poor performance. Try using `signature_match` instead! (Exception: Performance does not suffer if the entire method signature is exactly as specified in `pattern`. This provides an easy way to match full signatures with parameter and return types)
    - `parent`: Expects an extra property `inner` [Type] which contains a nested constraint to apply to the class holding the method;
    - `parameter`: Expects an extra properties `idx` and `inner` [Parameter] or [Type], matches when the idx-th parameter of the function or method matches the nested constraint inner;
    - `any_parameter`: Expects an optional extra property `start_idx` and `inner` [Parameter] or [Type], matches when there is any parameters (starting at start_idx) of the function or method matches the nested constraint inner;
    - `return`: Expects an extra property `inner` [Type] which contains a nested constraint to apply to the return of the method;
    - `is_static | is_constructor | is_native | has_code`: Accepts an extra property `value` which is either `true` or `false`. By default, `value` is considered `true`;
    - `number_parameters`: Expects an extra property `inner` [Integer] which contains a nested constraint to apply to the number of parameters (counting the implicit `this` parameter);
    - `number_overrides`: Expects an extra property `inner` [Integer] which contains a nested constraint to apply on the number of method overrides.

  - **Parameter:**

    - `parameter_has_annotation`: Expects an extra property `type` and an optional property `pattern`, respectively a string and a regex fully matching the value of the parameter annotation.

  - **Type:**

    - `extends`: Expects an extra property `inner` [Type] which contains a nested constraint that must apply to one of the base classes or itself. The optional property `include_self` is a boolean that tells whether the constraint must be applied on the type itself or not (defaults to `true`);
    - `super`: Expects an extra property `inner` [Type] which contains a nested constraint that must apply on the direct superclass;
    - `is_class | is_interface`: Accepts an extra property `value` which is either `true` or `false`. By default, `value` is considered `true`;

  - **Field**:

    - `signature`: Expects an extra property `pattern` which is a regex to fully match the full signature of the field. This is of the form `<className>.<fieldName>:<fieldType>`;
    - `parent`: Expects an extra property `inner` [Type] which contains a nested constraint to apply to the class holding the field;
    - `is_static`: Accepts an extra property `value` which is either `true` or `false`. By default, `value` is considered `true`;

  - **Method, Type or Field:**

    - `name`: Expects an extra property `pattern` which is a regex to fully match the name of the item;
    - `has_annotation`: Expects an extra property `type` and an optional property `pattern`, respectively a string and a regex fully matching the value of the annotation.
    - `visibility`: Expects an extra property `is` which is either `public`, `private` or `protected`; (Note this does not apply to `Field`)

  - **Integer:**

    - `< | <= | == | > | >= | !=`: Expects an extra property `value` which contains an integer that the input integer is compared with. The input is the left hand side.

  - **Any (Method, Parameter, Type, Field or Integer):**
    - `all_of`: Expects an extra property `inners` [Any] which is an array holding nested constraints which must all apply;
    - `any_of`: Expects an extra property `inners` [Any] which is an array holding nested constraints where one of them must apply;
    - `not`: Expects an extra property `inner` [Any] which contains a nested constraint that should not apply. (Note this is not yet implemented for `Field`s)

- `model`: A model, describing sources/sinks/propagations/etc.

  - **For method models**
    - `sources`\*: A list of sources, i.e a source *flowing out* of the method via return value or *flowing in* via an argument. To specify sources *flowing out* via an argument, specify it as `generations`. A source/generation has the following key/values:
      - `kind`: The source name;
      - `port`\*\*: The source access path (e.g, `"Return"` or `"Argument(1)"`);
      - `features`\*: A list of features/breadcrumbs names;
      - `via_type_of`\*: A list of ports;
    - `sinks`\*: A list of sinks, i.e describing that a parameter of the method flows into a sink. A sink has the following key/values:
      - `kind`: The sink name;
      - `port`: The sink access path (e.g, `"Return"` or `"Argument(1)"`);
      - `features`\*: A list of features/breadcrumbs names;
      - `via_type_of`\*: A list of ports;
    - `propagation`\*: A list of propagations (also called passthrough) that describe whether a taint on a parameter should result in a taint on the return value or another parameter. A propagation has the following key/values:
      - `input`: The input access path (e.g, `"Argument(1)"`);
      - `output`: The output access path (e.g, `"Return"` or `"Argument(2)"`);
      - `features`\*: A list of features/breadcrumbs names;
    - `attach_to_sources`\*: A list of attach-to-sources that describe that all sources flowing out of the method on the given parameter or return value must have the given features. An attach-to-source has the following key/values:
      - `port`: The access path root (e.g, `"Return"` or `"Argument(1)"`);
      - `features`: A list of features/breadcrumb names;
    - `attach_to_sinks`\*: A list of attach-to-sinks that describe that all sources flowing in the method on the given parameter must have the given features. An attach-to-sink has the following key/values:
      - `port`: The access path root (e.g, `"Argument(1)"`);
      - `features`: A list of features/breadcrumb names;
    - `attach_to_propagations`\*: A list of attach-to-propagations that describe that inferred propagations of sources flowing in or out of a given parameter or return value must have the given features. An attach-to-propagation has the following key/values:
      - `port`: The access path root (e.g, `"Return"` or `"Argument(1)"`);
      - `features`: A list of features/breadcrumb names;
    - `add_features_to_arguments`\*: A list of add-features-to-arguments that describe that flows that might flow on the given argument must have the given features. An add-features-to-argument has the following key/values:
      - `port`: The access path root (e.g, `"Argument(1)"`);
      - `features`: A list of features/breadcrumb names;
    - `modes`\*: A list of mode names that describe specific behaviors of a method;
    - `for_all_parameters`: Generate sources/sinks/propagations/attach*to*\* for all parameters of a method that satisfy some constraints. It accepts the following key/values:
      - `variable`: A symbolic name for the parameter;
      - `where`: An optional list of [Parameter] or [Type] constraints on the parameter;
      - `sources | sinks | propagation`: Same as under "model", but we accept the variable name as a parameter number.
  - `verbosity`\*: A logging level, to help debugging. 1 is the most verbose, 5 is the least. The default verbosity level is 5.

  - **For Field models**
    - `sources`\*: A list of sources the field should hold. A source has the following key/values:
      - `kind`: The source name;
      - `features`\*: A list of features/breadcrumbs names;
    - `sinks`\*: A list of sinks the field should hold. A sink has the following key/values:
      - `kind`: The sink name;
      - `features`\*: A list of features/breadcrumbs names;

In the above bullets,

- `*` denotes optional key/value.
- `**` denotes optional key/value. Default is `"Return"`.

Note, the implicit `this` parameter for methods has the parameter number 0.

### Development

#### When Sources or Sinks don't appear in Results

1. This could be because your model generator did not find any method matching your query. You can use the `"verbosity": 1` option in your model generator to check if it matched any method. For instance:

   ```json
   {
     "model_generators": [
       {
         "find": "methods",
         "where": /* ... */,
         "model": {
           /* ... */
         },
         "verbosity": 1
       }
     ]
   }
   ```

   When running mariana trench, this should print:

   ```
   INFO Method `...` satisfies all constraints in json model generator ...
   ```

2. Make sure that your model generator is actually running. You can use the `--verbosity 2` option to check that. Make sure your model generator is specified in `configuration/default_generator_config.json`.
3. You can also check the output models. Use `grep SourceKind models@*` to see if your source or sink kind exists. Use `grep 'Lcom/example/<class-name>;.<method-name>:' models@*` to see if a given method exists in the app.

<FbModels />


---
id: multi-source-sink-rules
title: Multi-Source, Multi-Sink Rules
sidebar_label: Multi-Source, Multi-Sink Rules
---

Multi-source multi-sink rules are used to track the flow of taint from multiple sources to multiple sinks. This can, for example, be useful if you want to track both the source types "SensitiveData" and "WorldReadableFileLocation" to an IO operation as displayed in the code below.

```java
File externalDir = context.getExternalFilesDir() // source WorldReadableFileLocation
String sensitiveData = getUserToken() // source SensitiveData

File outputFile = new File(externalDir, "file.txt");
try (FileOutputStream fos = new FileOutputStream(outputFile)) {
  fos.write(sensitiveData.getBytes()); // sink Argument(0) and Argument(1)
}
```

Such a rule can be defined as follows:

1. Define the sources as usual (see documentation above).
2. Define sinks on `FileOutputStream::write` as follows:

```json
{
  "model_generators": [
    {
      "find": "methods",
      "where": [ /* name = write */ ... ],
      "model": {
        "sink": [
          {
            "kind": "PartialExternalFileWrite",
            "partial_label": "outputStream",
            "port": "Argument(0)"
          },
          {
            "kind": "PartialExternalFileWrite",
            "partial_label": "outputBytes",
            "port": "Argument(1)"
          }
        ]
      }
    }
}
```

There are **two** sinks. There should always be as many sinks as there are sources, and the sinks must share the **same kind**. This looks almost like a regular sink definition, with an additional **partial_label** field. The `partial_label` field is used when defining the multi-source/sink rule below.

3. Define rules as follows:

```json
  {
    "name": "Experimental: Some name",
    "code": 9001,
    "description": "More description here.",
    "multi_sources": {
      "outputBytes": [
        "SensitiveData"
      ],
      "outputStream": [
        "WorldReadableFileLocation"
      ]
    },
    "partial_sinks": [
      "PartialExternalFileWrite"
    ]
}
```

Pay attention to how the labels and partial sink kinds match what is defined in the sinks above.

>**NOTE:** Multi-source/sink rules currently support exactly 2 sources/sinks only.


---
id: overview
title: Overview
sidebar_label: Overview
---
import {OssOnly, FbInternalOnly} from 'docusaurus-plugin-internaldocs-fb/internal';
import FbOverview from './fb/overview.md';

## What is Mariana Trench

**Mariana Trench** is a security focused static analysis platform targeting Android. The tool provides an extensible global taint analysis similar to pre-existing tools like [Pysa](https://pyre-check.org/docs/pysa-basics) for Python. The tool leverages existing static analysis infrastructure (e.g, [SPARTA](https://github.com/facebookincubator/SPARTA)) built on top of [Redex](https://github.com/facebook/redex).

By default Mariana Trench analyzes [dalvik bytecode](https://source.android.com/devices/tech/dalvik/dalvik-bytecode) and can work with or without access to the source code.

## Background

### Sources and Sinks

Under the context of taint analysis [1], "sources" usually mean sensitive data that originates from users. For example, sources can be users' passwords or locations. "Sinks" usually mean functions or methods that use data that "flows" from sources, where the term "flow" is generally defined under the context of "information flow" [2].
> An operation, or series of operations, that uses the value of some object, say x, to derive a value for another, say y, causes a flow from x to y

As an example, sinks can be a logging API that writes data into a log file.

### What does Mariana Trench do?

A flow from sources to sinks indicate that for example user passwords may get logged into a file, which is not desirable and is called as an **"issue"** under the context of Mariana Trench. Mariana Trench is designed to automatically discover such issues.

## Usage

The usage of Mariana Trench can be summarized in three steps:

<OssOnly>

1. Specify customized "sources" and "sinks". (See [Customize Sources and Sinks](./customize_sources_and_sinks.md))
2. Run Mariana Trench on an arbitrary Java repository (with the sources and sinks specified in Step 1), whether it be a repository for an Android application project or for a vanilla (or plain old) Java project.
3. View the analysis results from a web browser. (For steps 2 and 3 see [Getting Started](./getting_started.md))

</OssOnly>
<FbInternalOnly> <FbOverview/> </FbInternalOnly>

## References

1. [Tripp, Omer, et al. "TAJ: effective taint analysis of web applications." ACM Sigplan Notices 44.6 (2009): 87-97.](https://dl.acm.org/doi/10.1145/1542476.1542486)
2. [Denning, Dorothy E., and Peter J. Denning. "Certification of programs for secure information flow." Communications of the ACM 20.7 (1977): 504-513.](https://dl.acm.org/doi/10.1145/359636.359712)


---
id: rules
title: Rules
sidebar_label: Rules
---

import MultiSourceSinkRule from './multi_source_sink_rules.md';

<!-- Careful saving this file, weird formatting happens to json blocks -->

A rule describes flows that we want to catch (e.g, user input flowing into command execution).
A rule is made of a set of source [kinds](./models.md#kinds), a set of sink kinds, a name, a code, and a description.

Here is an example of a rule in JSON:
```json
{
  "name": "User input flows into code execution (RCE)",
  "code": 1,
  "description": "Values from user-controlled source may eventually flow into code execution",
  "sources": [
    "UserCamera",
    "UserInput",
  ],
  "sinks": [
    "CodeAsyncJob",
    "CodeExecution",
  ]
}
```

For guidance on modeling sources and sinks, see the next section, [Models and Model Generators](./models.md).

Rules used by Mariana Trench can be specified with the `--rules-paths` argument. The default set of rules that run can be found in [configuration/rules.json](https://github.com/facebook/mariana-trench/blob/main/configuration/rules.json).

### Transform Rules

Some flows are only interesting if they also pass through a specific method. These methods can be modeled as a propagation with transforms. Then, to catch these flows, we specify the ordered list of transforms here in the rule.

Here is an example of a transform rule in JSON:
```json
{
  "name": "URI Query Parameters flow into Internal Intent data",
  "code": 2,
  "oncall": "prodsec_mobile",
  "description": "Values from a query parameter source may eventually flow into Internal Intent data",
  "sources": [
    "UriQueryParameter"
  ],
  "transforms": [
    "IntentData"
  ],
  "sinks": [
    "LaunchingFamilyComponent"
  ]
}
```

The flow will only be created if UriQueryParameter flows through IntentData and then into LaunchingFamilyComponent. It will not be created when UriQueryParameter flows into LaunchingFamilyComponent without passing through the IntentData transform.

See [Models and Model Generators](./models.md#propagation-with-transforms) for how to model transforms.

<MultiSourceSinkRule />


---
id: shims
title: Shims
sidebar_label: Shims
---

import FbShims from './fb/shims.md';

## What is a "shim"?

We can think of a “shim” as the ability to say: "a call to a method matching
`<shimmed-method>` also implies calls to methods matching `<shim-target-1>`,
`<shim-target-2>`, …, `<shim-target-n>`.  This allows us to manually augment the
call-graph with artificial calls to methods at specific call-sites. This is
useful for simulating events in the android application by mimicking calls to
the known event-handlers which allows us to capture dataflows otherwise missed
due to the missing invocation of event-handlers.

For example, when a new fragment is added to a `FragmentManager`, the
`FragmentManager` is responsible for moving them through its lifecycle states
([reference](https://developer.android.com/guide/fragments/lifecycle#fragmentmanager)).
But we do not see the calls to the lifecycle event handlers on the new instance
of the fragment and can miss flows. We can define shims as follows to fill in
such missing links.

```java
class MainActivity extends AppCompatActivity {
    @Override
    protected void onCreate(Bundle savedinstanceState) {
        if (savedInstanceState == null) {
            Fragment myFragment = new MyFragment();
            // highlight-next-line
            myFragment.setArguments(getTaintedBundle());  // Source
            getSupportFragmentManager().beginTransaction()
                .setReorderingAllowed(true)
                // highlight-next-line
                .add(R.id.fragment_container_view, myFragment, null)  // FragmentManager handles `myFragment`'s lifecycle.
                .commit();
        }
    }
}

class MyFragment extends Fragment {
    @Override
    public void onCreate(Bundle savedInstanceState) {
        // highlight-next-line
        sink(getArguments()); // Issue if `mArguments` is tainted using `setArguments()`
    }
}
```

In this case, we can define a shim on `FragmentTransaction`'s `add()`  to
_trigger_ the lifecycle wrapper method of it's `Fragment` argument to mimic the
android's lifecycle management to catch this flow.

```json
{
    "find": "methods",
    "where": [
        {
            "constraint": "signature_pattern",
            "pattern": "Landroidx/fragment/app/FragmentTransaction;\\.add:\\(ILandroidx/fragment/app/Fragment;.*"
        }
    ],
    "shim": {
        "callees": [
            {
                "type_of": "Argument(2)",
                "lifecycle_name": "xfragment_lifecycle_wrapper"
            }
        ]
    }
},
```

## Terminologies
- shimmed-method: The method matching the `"where"` clause in the shim generator.
- shim-target: Method matching each of the `"callees"` object specified in the shim generator.
- parameters map: Mapping for arguments from shim-target to shimmed-method.

All callsites of the `shimmed-method` implies calls to all the `shim-targets`
specified with arguments propagated from the shimmed-method to shim-target based
on the parameters map.


## Specifying Shims
### Configuration file
The Mariana Trench binary consumes shim configuration files specified with the
argument `--shims-paths`. Each file contains a json array consisting of shim
definitions. Default set of shims can found in
[shims.json](https://github.com/facebook/mariana-trench/blob/main/configuration/shims.json)

### Shim Definition
Each shim definition object consists of the following keys:
- `find`: Currently only option is `methods`.
- `where`: A list of "constraints" which identifies the "shimmed-method". This is same as in [model generators](models.md#generators).
- `shim`: A list of "callees" each of which identifies a "shim-target". Each `callees` object needs to define the following:
  #### Receiver for the shim-target
  Receiver can be defined using one of the following keys:
  - `static`: Used to specify static methods as shim-targets.

    Expected value: A string specifying the dex class containing the shim-target method.

  - `type_of`: Used to specify an instance argument of the shimmed-method as the receiver.

    Expected value: A string specifying the _port_/_access path_ of the shimmed-method.

  - `reflected_type_of`: Used to specify a reflection argument of the shimmed-method as the receiver.

    Expected value: A string specifying the _port/access path_ of the shimmed-method. The type of the specified shimmed-method argument _must_ be: `Ljava/lang/Class;`.

  #### Method to call
  Method can be defined using one of the following keys:
  - `method_name`: Used to specify an existing method of the receiver as the shim-target.

    Expected value: A string specifying the dex proto of the method. This is of the form: `<method name>:(<parameter types>)<return type>`.

  - `lifecycle_name`: Used to specify lifecycle method specified using the option `--lifecycles-paths` as the shim-target.

    Expected value: A string matching the `method_name` specified in the lifecycle configuration.

  #### Parameters map (optional)
  A map specifying how the parameters of the shimmed-method should be propagated to the shim-target.
  If not specified, each argument of the shim-target is mapped to the first
  argument of the shimmed-method with the matching type.

  Expected format is as follows where the "key" refers to the shim-target and the value refers to the shimmed-method.
  ```json
  "parameters_map": {
      "Argument(<int>)": "Argument(<int>)",
      ...
  }
  ```

### Example
```java showLineNumbers
class TargetA {
    void methodA(Object o) {}
}

class TargetB {
    void methodB(Object o1, Object o2) {}
}

class TargetC {
    static void methodC(Object o) {}
}

class Shimmed {
    void shimMe(A a, Class b, Object o) {}
}

class Test {
    void test() {
        new Shimmed().shimMe(new TargetA(), TargetB.class, new Object());
    }
}
```

Shim definitions:

```json
{
    "find": "methods",
    "where": [
        {
            "constraint": "signature_pattern",
            "pattern": "LShimmed;\\.shimMe:\\(LTargetA;Ljava/lang/Class;Ljava/lang/Object;\\)V"
        }
    ],
    "shim": {
        "callees": [
            {
                "type_of": "Argument(1)",
                "method_name": "methodA:(Ljava/lang/Object;)V"
            },
            {
                "reflected_type_of": "Argument(2)",
                "method_name": "methodB:(Ljava/lang/Object;Ljava/lang/Object;)V",
                "parameters_map": {
                    "Argument(2)": "Argument(3)"
                }
            },
            {
                "static": "LTargetC;",
                "method_name": "method:C(Ljava/lang/Object;)V",
                "parameters_map": {
                    "Argument(0)": "Argument(3)"
                }
            }
        ]
    }
},
```
With this shim definition, the call to method `shimMe()` on line X will introduce calls to:
- `LTargetA.methodA:(Ljava/lang/Object;)V` where argument `o` is inferred to be `Argument(3)` of method `LShimmed;.shimMe:(LTargetA;Ljava/lang/Class;Ljava/lang/Object;)V`.
- `LTargetB.methodB:(Ljava/lang/Object;)V` where argument `o2` is mapped to `Argument(3)` of method `LShimmed;.shimMe:(LTargetA;Ljava/lang/Class;Ljava/lang/Object;)V` as specified. Note that argument `Class b` of the shimmed-method is resolved to be `TargetB` at the callsite.
- `LTargetC.methodC:()V` where argument `o` is mapped to `Argument(3)` of method `LShimmed;.shimMe:(LTargetA;Ljava/lang/Class;Ljava/lang/Object;)V` as specified. Note here that we specify `Argument(0)` of the shim-target in the parameters_map as this is a static method.

Note that when issues are found due to taint flow through shimmed-method to
shim-target, the trace following the call-site of the _shimmed-method_ will be
the _shim-target_ and a feature `via-shim:<shimmed-method>` will be introduced
at that point.

Sample shim definitions [here](https://github.com/facebook/mariana-trench/blob/main/source/tests/integration/end-to-end/code/shims/shims.json).

<FbShims />


