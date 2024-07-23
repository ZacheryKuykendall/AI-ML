# Folder Splitter Script

This Python script is designed to split a large folder containing many files into smaller chunks, each containing a specified number of files. It's particularly useful for preparing large file collections for upload to services with file count limitations, such as SharePoint.

## Features

- Splits a source folder into multiple chunk folders
- Allows customization of the number of files per chunk
- Moves files from the source folder to chunk folders
- Provides progress updates during execution

## Requirements

- Python 3.x (no additional packages required)

## Usage

1. Save the script as `folder_splitter.py`.

2. Open the script in a text editor and modify the following variables at the bottom of the file:

   ```python
   source_folder = "/path/to/your/source/folder"
   destination_folder = "/path/to/your/destination/folder"
   files_per_chunk = 25000
   ```

   - Set `source_folder` to the path of your folder containing the files to be split.
   - Set `destination_folder` to the path where you want the chunk folders to be created.
   - Adjust `files_per_chunk` if you need a different number of files per chunk.

3. Run the script:

   ```
   python folder_splitter.py
   ```

## How It Works

1. The script lists all files in the source folder.
2. It calculates the number of chunks needed based on the total file count and the specified files per chunk.
3. For each chunk:
   - A new folder is created in the destination directory.
   - Files are moved from the source folder to the chunk folder.
   - Progress is printed to the console.

## Notes

- This script moves files rather than copying them. This is faster and conserves disk space but alters the original folder structure.
- If you prefer to copy files instead of moving them, replace `shutil.move()` with `shutil.copy()` in the script.
- The script assumes all items in the source folder are files. Modify the script if you need to handle subdirectories.
- Depending on the number and size of files, this operation may take a considerable amount of time.

## Caution

Always backup your data before running scripts that move or modify files.

## Customization

You can modify the script to suit your specific needs. Some possible modifications include:
- Changing the naming convention for chunk folders
- Adding error handling for insufficient disk space or permissions issues
- Implementing logging instead of print statements for progress tracking

## Support

For issues, questions, or contributions, please [open an issue] or [submit a pull request] on the project's GitHub repository.