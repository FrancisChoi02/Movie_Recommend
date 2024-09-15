var NewComponent = React.createClass({
    render: function() {
      return (
        <div>
          <meta charSet="UTF-8" />
          <meta httpEquiv="X-UA-Compatible" content="IE=edge" />
          <meta name="viewport" content="width=device-width, initial-scale=1.0" />
          <title>Movie Recommend</title>

          <style dangerouslySetInnerHTML={{__html: "\n        /* 设置全局样式 */\n        * {\n            box-sizing: border-box;\n            transition: .2s;\n        }\n\n        /* 设置根元素变量 */\n        :root {\n            --bgColor: white;\n            /* 设置背景颜色变量为白色 */\n            --inputColor: black;\n            /* 设置输入框颜色变量为黑色 */\n            --outlineColor: rgb(60, 115, 235);\n            /* 设置输入框边框颜色变量为RGB(60, 115, 235) */\n            --border: black;\n        }\n\n        /* 设置body样式 */\n        body {\n            display: flex;\n            /* 设置body元素为flex布局 */\n            justify-content: center;\n            /* 水平居中对齐 */\n            align-items: center;\n            /* 垂直居中对齐 */\n            height: 100vh;\n            /* 设置body元素的高度为视口高度 */\n            overflow: hidden;\n            /* 隐藏溢出内容 */\n            background: var(--bgColor);\n            /* 设置背景颜色为变量--bgColor的值 */\n        }\n\n        /* 设置外层容器样式 */\n        .shell {\n            width: 100%;\n            /* 设置外层容器的宽度为100% */\n            height: 100vh;\n            /* 设置外层容器的高度为视口高度 */\n            display: flex;\n            /* 设置外层容器为flex布局 */\n            align-items: center;\n            /* 垂直居中对齐 */\n            justify-content: center;\n            /* 水平居中对齐 */\n            background-image: url(./img/1.png);\n            /* 设置背景图片为./img/1.png */\n            background-size: cover;\n            /* 背景图片等比例缩放铺满容器 */\n        }\n\n        /* 设置显示密码时的样式 */\n        body.show-password {\n            --bgColor: rgba(0, 0, 0, 0.9);\n            /* 设置背景颜色变量为RGBA(0, 0, 0, 0.9) */\n            --inputColor: white;\n            /* 设置输入框颜色变量为白色 */\n            --border: rgb(255, 255, 255);\n        }\n\n\n        /* 设置表单样式 */\n        form {\n            transform: translate3d(0, 0, 0);\n            /* 3D变换，无位移 */\n            padding: 50px;\n            /* 设置内边距为10px */\n            border: 20px solid var(--border);\n            border-radius: 10px;\n            box-shadow: 10px 10px 10px #00000065;\n        }\n\n        form>*+* {\n            margin-top: 15px;\n            /* 设置相邻元素之间的上边距为15px */\n        }\n\n        .form-item>*+* {\n            margin-top: 0.5rem;\n            /* 设置相邻元素之间的上边距为0.5rem */\n        }\n\n        /* 设置label, input, button样式 */\n        h2,\n        label,\n        input,\n        button {\n            font-size: 2rem;\n            /* 设置字体大小为2rem */\n            color: var(--inputColor);\n            /* 设置字体颜色为变量--inputColor的值 */\n            font-family: '优设标题黑';\n        }\n\n        h2 {\n            font-size: 4rem;\n            margin: 0;\n        }\n\n        label:focus,\n        input:focus,\n        button:focus {\n            outline-offset: 2px;\n            /* 设置聚焦时的外边距为2px */\n        }\n\n        label::-moz-focus-inner,\n        input::-moz-focus-inner,\n        button::-moz-focus-inner {\n            border: none;\n            /* 去掉Firefox浏览器的聚焦时的内边框 */\n        }\n\n        /* 设置密码相关样式 */\n        label[id=password],\n        input[id=password],\n        button[id=password] {\n            color: black;\n            /* 设置字体颜色为黑色 */\n        }\n\n        /* 设置按钮样式 */\n        button {\n            border: none;\n            /* 去掉按钮的边框 */\n        }\n\n        [id=submit] {\n            width: 100%;\n            cursor: pointer;\n            /* 设置鼠标样式为手型 */\n            margin: 20px 0 0 2px;\n            /* 设置外边距为20px 0 0 2px */\n            padding: 0.75rem 1.25rem;\n            /* 设置内边距为0.75rem 1.25rem */\n            color: var(--bgColor);\n            /* 设置字体颜色为变量--bgColor的值 */\n            background-color: var(--inputColor);\n            /* 设置背景颜色为变量--inputColor的值 */\n            box-shadow: 4px 4px 0 rgba(30, 144, 255, 0.2);\n            /* 设置阴影效果 */\n        }\n\n        [id=submit]:active {\n            transform: translateY(1px);\n            /* 设置点击时向下位移1px */\n        }\n\n        /* 设置输入框包裹器样式 */\n        .input-wrapper {\n            position: relative;\n            /* 设置相对定位 */\n        }\n\n        /* 设置输入框样式 */\n        input {\n            padding: 0.75rem 4rem 0.75rem 0.75rem;\n            /* 设置内边距为0.75rem 4rem 0.75rem 0.75rem */\n            width: 100%;\n            /* 设置宽度为100% */\n            border: 2px solid transparent;\n            /* 设置边为2px透明 */\n            border-radius: 0;\n            /* 设置边框圆角为0 */\n            background-color: transparent;\n            /* 设置背景颜色为透明 */\n            box-shadow: inset 0 0 0 2px black, inset 6px 6px 0 rgba(30, 144, 255, 0.2), 3px 3px 0 rgba(30, 144, 255, 0.2);\n            /* 设置阴影效果 */\n        \n        }\n\n        input:focus {\n            outline-offset: 1px;\n            /* 设置聚焦时的外边距为1px */\n        }\n\n        /* 设置显示密码时的输入框样式 */\n        .show-password input {\n            box-shadow: inset 0 0 0 2px black;\n            /* 设置阴影效果 */\n            border: 2px dashed white;\n            /* 设置边框为2px虚线白色 */\n        }\n\n        .show-password input:focus {\n            outline: none;\n            /* 去掉聚焦时的外边框 */\n            border-color: rgb(255, 255, 145);\n            /* 设置边框颜色为RGB(255, 255, 145) */\n        }\n\n        /* 设置眼睛按钮样式 */\n        [id=eyeball] {\n            --size: 1.25rem;\n            /* 设置变量--size的值为1.25rem */\n            display: flex;\n            /* 设置为flex布局 */\n            align-items: center;\n            /* 垂直居中对齐 */\n            justify-content: center;\n            /* 水平居中对齐 */\n            cursor: pointer;\n            /* 设置鼠标样式为手型 */\n            outline: none;\n            /* 去掉聚焦时的外边框 */\n            position: absolute;\n            /* 设置绝对定位 */\n            top: 50%;\n            /* 设置顶部距离为50% */\n            right: 0.75rem;\n            /* 设置右侧距离为0.75rem */\n            border: none;\n            /* 去掉边框 */\n            background-color: transparent;\n            /* 设置背景颜色为透明 */\n            transform: translateY(-50%);\n            /* 设置向上位移50% */\n        }\n\n        [id=eyeball]:active {\n            transform: translateY(calc(-50% + 1px));\n            /* 设置点击时向上位移50% + 1px */\n        }\n\n        .eye {\n            width: var(--size);\n            /* 设置宽度为变量--size的值 */\n            height: var(--size);\n            /* 设置高度为变量--size的值 */\n            border: 2px solid var(--inputColor);\n            /* 设置边框为2px实线，颜色为变量--inputColor的值 */\n            border-radius: calc(var(--size) / 1.5) 0;\n            /* 设置边框圆角为变量--size的值除以1.5，0 */\n            transform: rotate(45deg);\n            /* 设置旋转45度 */\n        }\n\n        .eye:before,\n        .eye:after {\n            content: \"\";\n            /* 清空内容 */\n            position: absolute;\n            /* 设置绝对定位 */\n            top: 0;\n            /* 设置顶部距离为0 */\n            right: 0;\n            /* 设置右侧距离为0 */\n            bottom: 0;\n            /* 设置底部距离为0 */\n            left: 0;\n            /* 设置左侧距离为0 */\n            margin: auto;\n            /* 设置自动外边距 */\n            border-radius: 100%;\n            /* 设置边框圆角为100% */\n        }\n\n        .eye:before {\n            width: 35%;\n            /* 设置宽度为35% */\n            height: 35%;\n            /* 设置高度为35% */\n            background-color: var(--inputColor);\n            /* 设置背景颜色为变量--inputColor的值 */\n        }\n\n        .eye:after {\n            width: 65%;\n            /* 设置宽度为65% */\n            height: 65%;\n            /* 设置高度为65% */\n            border: 2px solid var(--inputColor);\n            /* 设置边框为2px实线，颜色为变量--inputColor的值 */\n            border-radius: 100%;\n            /* 设置边框圆角为100% */\n        }\n\n        /* 设置光束样式 */\n        [id=beam] {\n            position: absolute;\n            /* 设置绝对定位 */\n            top: 50%;\n            /* 设置顶部距离为50% */\n            right: 1.75rem;\n            /* 设置右侧距离为1.75rem */\n            clip-path: polygon(100% 50%, 100% 50%, 0 0, 0 100%);\n            /* 设置剪切路径为多边形 */\n            width: 100vw;\n            /* 设置宽度为100vw */\n            height: 25vw;\n            /* 设置高度为25vw */\n            z-index: 1;\n            /* 设置层级为1 */\n            mix-blend-mode: multiply;\n            /* 设置混合模式为multiply */\n            transition: transform 200ms ease-out;\n            /* 设置过渡效果为200ms的ease-out */\n            transform-origin: 100% 50%;\n            /* 设置变换原点为右侧50% */\n            transform: translateY(-50%) rotate(var(--beamDegrees, 0));\n            /* 设置向上位移50%并旋转--beamDegrees度 */\n            pointer-events: none;\n            /* 禁用指针事件 */\n        }\n\n        .show-password [id=beam] {\n            background: rgb(255, 255, 145);\n            /* 设置背景颜色为RGB(255, 255, 145) */\n        }\n    " }} />
          
          <div className="shell">
            <form>
              <h2>LOGIN</h2>
              <div className="form-item">
                <label htmlFor="username">Username</label>
                <div className="input-wrapper">
                  <input type="text" id="username" autoComplete="off" autoCorrect="off" autoCapitalize="off" spellCheck="false" data-lpignore="true" />
                </div>
              </div>
              <div className="form-item">
                <label htmlFor="password">Password</label>
                <div className="input-wrapper">
                  <input type="password" id="password" autoComplete="off" autoCorrect="off" autoCapitalize="off" spellCheck="false" data-lpignore="true" />
                  <button type="button" id="eyeball">
                    <div className="eye" />
                  </button>
                  <div id="beam" />
                </div>
              </div>
              <button id="submit">Sign in</button>
            </form>
          </div>
        </div>
      );
    }
  });