# Astric
Next generation CSS.

```
 █████╗ ███████╗████████╗██████╗ ██╗ ██████╗
██╔══██╗██╔════╝╚══██╔══╝██╔══██╗██║██╔════╝
███████║███████╗   ██║   ██████╔╝██║██║     
██╔══██║╚════██║   ██║   ██╔══██╗██║██║     
██║  ██║███████║   ██║   ██║  ██║██║╚██████╗
╚═╝  ╚═╝╚══════╝   ╚═╝   ╚═╝  ╚═╝╚═╝ ╚═════╝
```

## Table of Contents
- [Astric](#astric)
  - [Features](#features)
  - [Syntax](#syntax)
  - [Usage](#usage)

## Features

Astric is a lightweight CSS preprocessor that simplifies the way you write CSS. It offers the following features:

- **Python-like Syntax:** Write CSS using a Python-like syntax.
- **Simplicity:** Write clean, maintainable, and scalable CSS.
- **Optionals:** Semicolons are optional. If you want to use them, you can (and is required for single-line properties).
- **Variables:** Define reusable values using the `$` symbol.
- **Loops:** Generate repetitive CSS with ease using `--for` and `--endfor`.
- **Comments:** Add comments to your Astric files.
- **Compact Output:** Use the `--compact` flag to compact outputted CSS onto one line.

## Syntax

Astric introduces a simple and powerful syntax to enhance your CSS workflow. Here are some key features:

### Variables
Define reusable values using the `$` symbol.
```Astric
$primary-color: #3498db;
$spacing: 16px;

body
    color: $primary-color;
    margin: $spacing;
```

### Loops
Generate repetitive CSS with ease using `--for` and `--endfor`.
```Astric
--for $i from 1 to 3
    .item-$i
        width: calc(100% / $i)
--endfor
```

### Comments
Add comments to your Astric files. Comments will be stripped out in the generated CSS.
```Astric
// Singleline comment
>> Another singleline comment
```

These features make Astric a powerful tool for writing clean, maintainable, and scalable CSS.


## Usage

To use Astric, follow these steps:

1. **Download the library**:
    ```sh
    pip3 install Astric
    ```

2. **Prepare your `.astr` file**:
    Create a `.astr` file with your Astric syntax. For example, create a file named `example.astr`:
    ```Astric
    $primary-color: #3498db
    $spacing: 16px

    body
        color: $primary-color
        margin: $spacing

    --for $i from 1 to 3
        .item-$i
            width: calc(100% / $i)
    --endfor
    ```

3. **Run Astric**:
    Use the `Astric` command to process your `.astr` file and generate the corresponding CSS file:
    ```sh
    Astric example.astr output.css
    ```

4. **Check the output**:
    The generated CSS will be written to `output.css`. You can open this file to see the processed CSS:
    ```css
    body {
        color: #3498db;
        margin: 16px;
    }

    .item-1 {
        width: calc(100% / 1);
    }
    .item-2 {
        width: calc(100% / 2);
    }
    .item-3 {
        width: calc(100% / 3);
    }
    ```

5. **Compact** (optional):
    You can use the `--compact` flag to compact outputted CSS onto one line.
