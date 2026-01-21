# Claude Code Skills

A collection of custom skills for [Claude Code](https://claude.ai/claude-code).

## Skills

### slide-generator

Generates professional presentation slides from any content using Google's Gemini image generation API. Uses a two-pass approach:

1. **Story Agent** - Analyzes source material and creates a structured storyboard
2. **Design Agent** - Creates visual specifications and generates slides

**Requirements:** `GEMINI_API_KEY` environment variable

### second-opinion

Queries GPT-5.2 Pro and Gemini 3 Pro in parallel to get alternative perspectives on Claude's outputs. Useful for validating answers, exploring alternative approaches, or comparing responses across models.

**Requirements:** `OPENAI_API_KEY` and `GEMINI_API_KEY` environment variables, `aiohttp` package

## Installation

Clone this repository into your Claude Code skills directory:

```bash
git clone <repo-url> ~/.claude/skills
```

## Usage

Once installed, invoke skills in Claude Code using:

- `/slide-generator` - Create presentation slides
- `/second-opinion` - Get multi-model comparison

## License

MIT License

Copyright (c) 2026 Luca Fiaschi

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
