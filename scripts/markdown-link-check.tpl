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
            "pattern": "^(?!(/|/media/))",
            "replacement": "/ERROR:link-must-start-with-slash:"
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
