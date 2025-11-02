from flask import Flask, render_template, request

app = Flask(__name__)

DAYS = 3  # 3日分

YOUHIN_LIST = {
    "common": [
        "水", "食品", "防災ヘルメット", "衣類下着", "レインウェア", "ズック靴",
        "懐中電灯", "携帯ラジオ", "予備電池携帯充電器", "マッチろうそく",
        "救急用品", "使い捨てカイロ", "ブランケット", "軍手",
        "洗面用具", "歯ブラシ歯磨き粉", "タオル", "ペンノート"
    ],
    "female": ["生理用品", "サニタリーショーツ", "防犯ブザー", "おりものシート", "中身の見えないゴミ袋"],
    "child": ["ミルク", "子供用紙おむつ", "抱っこ紐", "使い捨て哺乳瓶", "おしりふき", "子供の靴",
              "離乳食", "携帯用おしり洗浄機", "携帯カトラリー", "ネックライト"],
    "elderly": ["大人用紙ぱんつ", "介護食", "デリケートゾーンの洗浄剤", "杖",
                "入れ歯洗浄剤", "持病の薬", "補聴器", "吸引パッド", "おくすり手帳"]
}


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        num_people = int(request.form["num_people"])
        return render_template("form.html", num_people=num_people)
    return render_template("index.html")


@app.route("/result", methods=["POST"])
def result():
    people = []
    i = 0
    while f"age{i}" in request.form:
        age = int(request.form[f"age{i}"])
        sex = request.form[f"sex{i}"]
        weight = float(request.form.get(f"weight{i}", 50))
        people.append({"age": age, "sex": sex, "weight": weight})
        i += 1

    all_results = []
    total_items = {}
    total_water_l = 0
    total_calories = 0

    for person in people:
        age = person["age"]
        sex = person["sex"]
        weight = person["weight"]

        calories = 0
        water = 0
        personal_items = []

        # 共通用品
        personal_items.extend(YOUHIN_LIST["common"])

        # 性別・年齢別用品
        if sex == "female":
            personal_items.extend(YOUHIN_LIST["female"])
            if age < 5:
                personal_items.extend(YOUHIN_LIST["child"])
            elif age >= 66:
                personal_items.extend(YOUHIN_LIST["elderly"])
        elif sex == "male":
            if age < 5:
                personal_items.extend(YOUHIN_LIST["child"])
            elif age >= 66:
                personal_items.extend(YOUHIN_LIST["elderly"])

        # カロリー・水分計算
        if sex == "female":
            if age < 1:
                water += weight * 0.15
            elif age == 1:
                calories += 59.7 * weight
                water += weight * 0.15
            elif 1 < age <= 2:
                calories += 59.7 * weight
                water += weight * 0.1
            elif 3 <= age <= 5:
                calories += 52.2 * weight
                water += weight * 0.1
            elif 6 <= age <= 7:
                calories += 41.9 * weight
                water += weight * 0.08
            elif 8 <= age <= 9:
                calories += 38.3 * weight
                water += weight * 0.08
            elif 10 <= age <= 11:
                calories += 34.8 * weight
                water += weight * 0.08    
            elif 12 <= age <= 14:
                calories += 29.6 * weight
                water += weight * 0.08 
            elif 15 <= age <= 17:
                calories += 25.3 * weight
                water += weight * 0.08 
            elif 18 == age :
                calories += 22.1 * weight
                water += weight * 0.08 
            elif 19 <= age <= 29:
                calories += 22.1 * weight
                water += weight * 0.05
            elif 30 <= age <= 49:
                calories += 21.7 * weight
                water += weight * 0.05
            elif 50 <= age <= 65:
                calories += 20.7 * weight
                water += weight * 0.05
            elif age >= 66:
                calories += 20.7 * weight
                water += weight * 0.04
        elif sex == "male":
            if age < 1:
                water += weight * 0.15
            elif age == 1:
                calories += 61 * weight
                water += weight * 0.15
            elif 1 < age <= 2:
                calories += 61 * weight
                water += weight * 0.1
            elif 3 <= age <= 5:
                calories += 54.8 * weight
                water += weight * 0.1
            elif 6 <= age <= 7:
                calories += 44.3 * weight
                water += weight * 0.08
            elif 8 <= age <= 9:
                calories += 40.8 * weight
                water += weight * 0.08
            elif 10 <= age <= 11:
                calories += 37.4 * weight
                water += weight * 0.08    
            elif 12 <= age <= 14:
                calories += 31.0 * weight
                water += weight * 0.08 
            elif 15 <= age <= 17:
                calories += 27 * weight
                water += weight * 0.08 
            elif 18 == age :
                calories += 24 * weight
                water += weight * 0.08 
            elif 19 <= age <= 29:
                calories += 24 * weight
                water += weight * 0.05
            elif 30 <= age <= 49:
                calories += 22.3 * weight
                water += weight * 0.05
            elif 50 <= age <= 65:
                calories += 21.5 * weight
                water += weight * 0.05
            elif age >= 66:
                calories += 21.5 * weight
                water += weight * 0.04

        all_results.append({
            "age": age,
            "sex": sex,
            "weight": weight,
            "calories": int(calories * DAYS),
            "water_l": round(water * DAYS, 2),
            "items_list": personal_items
        })

        # 総合カウントに追加
        for item in personal_items:
            total_items[item] = total_items.get(item, 0) + 1

        total_water_l += water * DAYS
        total_calories += calories * DAYS

    return render_template(
        "result.html",
        all_results=all_results,
        total_items=total_items,
        total_water_l=round(total_water_l, 2),
        total_calories=int(total_calories)
    )


if __name__ == "__main__":
    app.run(debug=True)

