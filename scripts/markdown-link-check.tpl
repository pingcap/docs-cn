{
    "ignorePatterns": [
        {
            "pattern": "^(http|https|ftp|mailto):"
        },
        {
            "pattern": "\\.\\./media/"
        }
    ],
    "replacementPatterns": [
        {
            "pattern": "^(?!(\\.|/media/))",
            "replacement": "<DOC_ROOT>/"
        },
        {
            "pattern": "^/media/",
            "replacement": "<ROOT>/media/"
        },
        {
            "pattern": "#.+",
            "replacement": ""
        }
    ]
}
