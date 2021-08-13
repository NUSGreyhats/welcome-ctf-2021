var gate1 = (key) => {
    if (key == "1ts") return true;
    return false;
}

var gate2 = (key) => {
    if (key.length != 6)  return false;
    if ((key.charCodeAt(0) ^ "Chicken".charCodeAt(0)) != 0x20) return false;
    if ((key.charCodeAt(1) ^ "Doughnut".charCodeAt(4)) != 0x58) return false;
    if ((key.charCodeAt(2) ^ "Fruit".charCodeAt(3)) != 0x04) return false;
    if ((key.charCodeAt(3) ^ "Icecream".charCodeAt(5)) != 0x54) return false;
    if ((key.charCodeAt(4) ^ "Sausage".charCodeAt(3)) != 0x1d) return false;
    if ((key.charCodeAt(5) ^ "Durian".charCodeAt(4)) != 0x06) return false;
    return true;
}

var gate3 = (key) => {
    if (key.length != 2) return false;
    var c0 = key.charCodeAt(0);
    var c1 = key.charCodeAt(1);
    if (c0 > c1 && c0 + c1 == 164 && c0 * c1 == 5568) return true;
    return false;
}

var gate4 = (key) => {
    if (key.length != 4) return false;

    var rs = [2, 3, 4, 5];
    var target = [201, 129, 214, 102];
    for (var i = 0; i < 4; ++i) {
        var r = rs[i];
        var c = key.charCodeAt(i);
        if ((((c << r) & 0xff) | (c >> (8 - r))) != target[i]) return false;
    }

    return true;
}

var level = 1;
var flag = "greyhats{";

$(document).ready(() => {
    $("#input").keyup(function (e) {
        if (e.keyCode != 13) return;

        var input = $("#input").val();

        if (level == 1) {
            if (gate1(input)) {
                $("#result").text("Correct! Now onto Gate 2!");
                $("#input-text").text("Gate 2!");
                $("#input").val("");
                flag += input + "_";
                level++;
            } else {
                $("#result").text("Wrong key! Try again!");
            }
        } else if (level == 2) {
            if (gate2(input)) {
                $("#result").text("Correct! Now onto Gate 3!");
                $("#input-text").text("Gate 3!");
                $("#input").val("");
                flag += input + "_";
                level++;
            } else {
                $("#result").text("Wrong key! Try again!");
            }
        } else if (level == 3) {
            if (gate3(input)) {
                $("#result").text("Correct! Now onto Gate 4!");
                $("#input-text").text("Gate 4!");
                $("#input").val("");
                flag += input + "_";
                level++;
            } else {
                $("#result").text("Wrong key! Try again!");
            }
        } else if (level == 4) {
            if (gate4(input)) {
                flag += input + "}";
                $("#result").text(flag);
                $("#input-text").hide();
                $("#input").hide();
            } else {
                $("#result").text("Wrong key! Try again!");
            }
        }
    });
})