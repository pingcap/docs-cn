{
    "ignorePatterns": [
        {
            "pattern": "^(http|https|ftp|mailto):"
        },
        {
            "pattern": "\\.\\./media/"
        },
        {
            "comment": "anchors to current file are ignored",
            "pattern": "^#.+$"
        }
    ],
    "replacementPatterns": [
        {
            "pattern": "^(?!(/<VERSION>/|/media/))",
            "replacement": "/ERROR:link-must-start-with-slash-and-cannot-reference-files-in-other-version-directory:"
        },
        {
            "comment": "prefix with repo root",
            "pattern": "^(?!(\\.|/ERROR:.*))",
            "replacement": "<ROOT>/"
        },
        {
            "comment": "remove anchor part",
            "pattern": "#.+$",
            "replacement": ""
        }
    ]
}
