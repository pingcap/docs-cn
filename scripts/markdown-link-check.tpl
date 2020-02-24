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
