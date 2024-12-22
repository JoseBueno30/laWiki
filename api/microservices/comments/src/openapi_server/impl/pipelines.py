# Removes ObjectID fields and converts them to string
pipeline_remove_id = [
    {'$addFields': {"id": {'$toString': '$_id'},
                    "article_id": {'$toString': '$article_id'},
                    "author.id": {'$toString': '$author._id'}
                    }
     },
    {'$unset': ["_id", "author._id"]}  # Remove the original _id fields
]

pipeline_trunc_date = [
    {
        "$set": {
            "creation_date": {
                "$dateFromParts": {
                    "year": {"$year": "$creation_date"},
                    "month": {"$month": "$creation_date"},
                    "day": {"$dayOfMonth": "$creation_date"}
                }
            }
        }
    }
]

# Groups all comments in a list
pipeline_group_comments = [
    {"$group": {
        "_id": None,
        "comments": {"$push": "$$ROOT"},
    }},
    {
        "$project": {
            "_id": 0,
        }
    }
]