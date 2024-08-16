# ReMarkable Highlight Extractor 📚✨

The ReMarkable is an E-Ink tablet primarily used for reading and note-taking. 

One of my main uses for the tablet is loading PDFs and using the snap-to-text highlighting feature. However, as of now, there isn't a mainstream method to extract the text that has been highlighted. While there have been various GitHub repositories dedicated to extracting highlighted text by parsing the underlying files, these methods worked well for older versions but have become obsolete with recent updates, as the ReMarkable changed how it stores annotation information.

Given this, I decided to take a different approach with my project to address the problem effectively. 🎯
## My Approach 💡

Rather than trying to parse the underlying files, my program focuses on keeping the highlights in context by extracting entire pages that contain yellow highlights. This way, you retain the full context of the highlighted content rather than isolating the text.
## Cloning the Repository 🛠️

To get started, clone the repository using the following command:

```
git clone https://github.com/yourusername/remarkable-highlight-extractor.git
cd remarkable-highlight-extractor
```

## Program Options ⚙️

When running the program, you can customize its behavior using various options:

    highlighted (required): The path to the PDF with the highlights.
    output (required): The path where the output PDF with extracted pages will be saved.
    -s, --start: The starting page number for extraction (default is 0, meaning it starts from the first page).
    -e, --end: The ending page number for extraction (default is 0, which processes until the last page).
    -n, --numbering: The page number where numbering starts relative to the PDF file (default is 1).
    -d, --display: Option to display the page images during processing (use this flag if needed).
    -b, --blanks: Option to display pages even if no highlights are detected (use this flag if you want to review non-highlighted pages).

## Example Usage 🚀

To run the program with a specific set of options, use a command like the following:
```
python extract.py highlighted.pdf output.pdf -s 1 -e 10 -d -b
```
This command will extract pages 1 to 10 from highlighted.pdf, save the output to output.pdf, display each page as it processes, and even show pages without highlights.
