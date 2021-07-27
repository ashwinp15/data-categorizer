import pandas as pd
from flask import send_file
import zipfile
import shutil

def paymentFilter(filename):
    data = pd.read_csv(filename)
    free = data[data['Type'] == 'Free']
    paid= data[data['Type'] == 'Paid']

    with zipfile.ZipFile('outputs/paymentFilterOutput.zip', 'w') as csv_zip:
        csv_zip.writestr("free.csv", free.to_csv())
        csv_zip.writestr("paid.csv", paid.to_csv())


    return send_file("outputs/paymentFilterOutput.zip",
                        mimetype='zip',
                        attachment_filename='paymentFilterOutput.zip',
                        as_attachment=True)


def contentRatingFilter(filename):
    data = pd.read_csv(filename)
    categories = list(data['Content Rating'].dropna().unique())
    print(categories)
    with zipfile.ZipFile('outputs/contentRatingFilterOutput.zip', 'w') as csv_zip:
        for categ in categories:
            filtered = data[data['Content Rating'] == categ]
            csv_zip.writestr("{}.csv".format(categ), filtered.to_csv())

    return send_file("outputs/contentRatingFilterOutput.zip",
                        mimetype='zip',
                        attachment_filename='contentRatingFilterOutput.zip',
                        as_attachment=True)


def roundOffRatings(filename):
    data = pd.read_csv(filename).dropna()
    fn = lambda row: round(row.Rating)
    col = data.apply(fn, axis=1)
    data = data.assign(Rounded_Ratings=col.values)
    data.to_csv("outputs/roundOffResult.csv")

    return send_file("outputs/roundOffResult.csv",
                        mimetype='text/csv',
                        attachment_filename='roundOffResult.csv',
                        as_attachment=True)

