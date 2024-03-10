# aihub



## img_change_color(改底色)

```json
url: ai/change_bg_color
method: post
post data:
{
    "base64_img": "", // 图片的base64 encode后发送
    "color": "blue"
}

return data:
{
    "data":"base64 encode img"
}
```

## get_id_card_img(转证件照模版)

```json
url: ai/get_id_card_img
method: post
post data:

{
    "base64_img": "", // 图片的base64 encode后发送
    "inch_choice": 1 // 目前可选  1: 1寸， 2: 2寸， 3： 小2寸
}

return data:
{
    "data":"base64 encode img"
}
```