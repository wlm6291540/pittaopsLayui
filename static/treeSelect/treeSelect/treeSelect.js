layui.define(['tree', 'form', 'jquery'], function (exports) {
    "use strict";

    var $ = layui.$,
        form = layui.form,
        tree = layui.tree,
        MOD_NAME = 'treeSelect';
    var TreeSelect = function () {
        this.v = '1.0.1';
    };

    TreeSelect.prototype.render = function (options) {
        var elem = options.elem,
            //请求地址
            data = options.data,
            //请求方法GET POST
            type = options.type,
            //请求头
            headers = options.headers,
            //输入框提示文字
            placeholder = options.placeholder,
            //自定义节点唯一标识名称（索引）
            key = options.key || 'id',
            // 是否显示复选框
            showCheckbox = options.showCheckbox || false,
            //定义默认选中的节点集合，值对应的是 key，需开启 showCheckbox 参数
            checked = options.checked || [],
            //定义默认展开节点集合，值对应的是 key。用法同 checked
            spread = options.spread || [],
            //是否开启节点的操作图标
            edit = options.edit || false,
            //是否开启手风琴模式，默认 false
            accordion = options.accordion || false,
            //是否仅允许节点左侧图标控制展开收缩。
            onlyIconControl = options.onlyIconControl || true,
            //是否允许点击节点时弹出新窗口跳转。默认 false
            isJump = options.isJump || false,
            //是否开启连接线。默认 false
            showLine = options.showLine || false,
            //节点默认名称。一般添加节点时的默认名称
            defaultNodeName = options.defaultNodeName || '未命名',
            //自定义数据为空时的文本
            emptyText = options.emptyText || '暂无数据',
            // 节点点击回调
            click = options.click,
            // 渲染成功后的回调函数
            success = options.success,
            // 设置高度
            height = options.height,
            // 唯一id
            tmp = new Date().getTime(),
            DATA = {},
            selected = 'layui-form-selected',
            TREE_OBJ = undefined,
            TREE_INPUT_ID = 'treeSelect-input-' + tmp,
            TREE_INPUT_CLASS = 'layui-treeselect',
            TREE_SELECT_ID = 'layui-treeSelect-' + tmp,
            TREE_SELECT_CLASS = 'layui-treeSelect',
            TREE_SELECT_TITLE_ID = 'layui-select-title-' + tmp,
            TREE_SELECT_TITLE_CLASS = 'layui-select-title',
            TREE_SELECT_BODY_ID = 'layui-treeSelect-body-' + tmp,
            TREE_SELECT_BODY_CLASS = 'layui-treeSelect-body',
            TREE_SELECT_SEARCHED_CLASS = 'layui-treeSelect-search-ed';

        var a = {
            init: function () {
                $.ajax({
                    url: data,
                    type: type,
                    headers: headers,
                    dataType: 'json',
                    success: function (d) {
                        DATA = d;
                        a.hideElem().input().toggleSelect().loadCss().preventEvent();
                        a.initTree(d);

                        if (success) {
                            var obj = {
                                treeId: TREE_SELECT_ID,
                                data: d
                            };
                            success(obj);
                        }
                    }
                });
                return a;
            },
            initTree: function (d) {
                TREE_OBJ = tree.render({
                    elem: '#' + TREE_SELECT_BODY_ID
                    , data: d
                    , showCheckbox: showCheckbox  //是否显示复选框
                    , key: key  //定义索引名称
                    , checked: checked  //选中节点(依赖于 showCheckbox 以及 key 参数)。
                    , spread: spread  //展开节点(依赖于 key 参数)
                    , edit: edit
                    , accordion: accordion //是否开启手风琴模式
                    , onlyIconControl: onlyIconControl
                    , isJump: isJump //是否允许点击节点时弹出新窗口跳转
                    , showLine: showLine
                    , defaultNodeName: defaultNodeName
                    , emptyText: emptyText
                    , click: function (obj) {
                        a.onClick(obj);
                    }
                });
                return TREE_OBJ;
            },
            onCollapse: function () {
                a.focusInput();
            },
            onExpand: function () {
                a.focusInput();
            },
            focusInput: function () {
                $('#' + TREE_INPUT_ID).focus();
            },
            onClick: function (obj) {
                var name = obj.data.label;
                var id = obj.data.id;
                var $input = $('#' + TREE_INPUT_ID);
                $input.val(name);
                $(elem).attr('value', id).val(id);
                $('#' + TREE_SELECT_ID).removeClass(selected);

                if (click) {
                    var obj = {
                        data: DATA,
                        treeId: TREE_SELECT_ID
                    };
                    click(obj);
                }
                return a;
            },
            hideElem: function () {
                $(elem).hide();
                return a;
            },
            input: function () {
                var readonly = 'readonly';
                var selectHtml = '<div class="' + TREE_SELECT_CLASS + ' layui-unselect layui-form-select" id="' + TREE_SELECT_ID + '">' +
                    '<div class="' + TREE_SELECT_TITLE_CLASS + '" id="' + TREE_SELECT_TITLE_ID + '">' +
                    ' <input type="text" id="' + TREE_INPUT_ID + '" placeholder="' + placeholder + '" value="" ' + readonly + ' class="layui-input layui-unselect">' +
                    '<i class="layui-edge"></i>' +
                    '</div>' +
                    '<div class="layui-anim layui-anim-upbit" style="max-height: ' + height + '">' +
                    '<div class="' + TREE_SELECT_BODY_CLASS + '" id="' + TREE_SELECT_BODY_ID + '"></div>' +
                    '</div>' +
                    '</div>';
                $(elem).parent().append(selectHtml);
                return a;
            },
            /**
             * 展开/折叠下拉框
             */
            toggleSelect: function () {
                var item = '#' + TREE_SELECT_TITLE_ID;
                a.event('click', item, function (e) {
                    var $select = $('#' + TREE_SELECT_ID);
                    if ($select.hasClass(selected)) {
                        $select.removeClass(selected);
                        $('#' + TREE_INPUT_ID).blur();
                    } else {
                        // 隐藏其他picker
                        $('.layui-form-select').removeClass(selected);
                        // 显示当前picker
                        $select.addClass(selected);
                    }
                    e.stopPropagation();
                });
                $(document).click(function () {
                    var $select = $('#' + TREE_SELECT_ID);
                    if ($select.hasClass(selected)) {
                        $select.removeClass(selected);
                        $('#' + TREE_INPUT_ID).blur();
                    }
                });
                return a;
            },
            checkNodes: function (nodes) {
                for (var i = 0; i < nodes.length; i++) {
                    var o = nodes[i],
                        pid = o.parentTId,
                        tid = o.tId;
                    if (pid !== null) {
                        // 获取父节点
                        $('#' + pid).addClass(TREE_SELECT_SEARCHED_CLASS);
                        var pNode = TREE_OBJ.getNodesByParam("tId", pid, null);
                        TREE_OBJ.expandNode(pNode[0], true, false, true);
                    }
                    $('#' + tid).addClass(TREE_SELECT_SEARCHED_CLASS);
                }
            },
            // 阻止Layui的一些默认事件
            preventEvent: function () {
                var item = '#' + TREE_SELECT_ID + ' .layui-anim';
                a.event('click', item, function (e) {
                    e.stopPropagation();
                });
                return a;
            },
            loadCss: function () {
                var ext = '.layui-treeSelect .ztree li span.button{font-family:layui-icon!important;font-size:16px;font-style:normal;-webkit-font-smoothing:antialiased;-moz-osx-font-smoothing:grayscale;background:none;line-height:inherit;}.layui-treeSelect .ztree li span.button.ico_open{display:none;}.layui-treeSelect .ztree li span.button.ico_close{display:none;}.layui-treeSelect .ztree li span.button.ico_docu:before{content:"\\e621";}.layui-treeSelect .ztree li span.button.bottom_close:before,.layui-treeSelect .ztree li span.button.center_close:before,.layui-treeSelect .ztree li span.button.roots_close:before,.layui-treeSelect .ztree li span.button.root_close:before{content:"\\e623";}.layui-treeSelect .ztree li span.button.bottom_open:before,.layui-treeSelect .ztree li span.button.roots_open:before,.layui-treeSelect .ztree li span.button.center_open:before,.layui-treeSelect .ztree li span.button.root_open:before{content:"\\e625";}.layui-treeSelect .ztree li a:hover{text-decoration:none;}.layui-treeSelect .ztree *{font-size:14px;}.layui-treeSelect .ztree li{line-height:inherit;padding:2px 0;}.layui-treeSelect .ztree li span.button.switch{position:relative;top:-1px;}.layui-treeSelect .ztree li a,.ztree li span{line-height:18px;height:inherit;}.layui-treeSelect .ztree li a.curSelectedNode{color:#5FB878;background:none;border:none;height:inherit;padding-top:1px;}.layui-treeSelect .layui-anim::-webkit-scrollbar{width:6px;height:6px;background-color:#F5F5F5;}.layui-treeSelect .layui-anim::-webkit-scrollbar-track{box-shadow:inset 0 0 6px rgba(107,98,98,0.3);border-radius:10px;background-color:#F5F5F5;}.layui-treeSelect .layui-anim::-webkit-scrollbar-thumb{border-radius:10px;box-shadow:inset 0 0 6px rgba(107,98,98,0.3);background-color:#555;}.layui-treeSelect.layui-form-select .layui-anim{display:none;position:absolute;left:0;top:42px;padding:5px 0;z-index:9999;min-width:100%;border:1px solid #d2d2d2;max-height:160px;overflow-y:auto;background-color:#fff;border-radius:2px;box-shadow:0 2px 4px rgba(0,0,0,.12);box-sizing:border-box;}.layui-treeSelect.layui-form-selected .layui-anim{display:block;}.layui-treeSelect .ztree li ul.line{background:none;position:relative;}.layui-treeSelect .ztree li ul.line:before{content:"";height:100%;border-left:1px dotted #ece;position:absolute;left:8px;}.layui-treeSelect .ztree li .center_docu:before,.ztree li .bottom_docu::before{content:"";height:100%;border-left:1px dotted #ece;position:absolute;left:8px;}.layui-treeSelect .ztree li .center_docu::after,.ztree li .bottom_docu::after{content:"";position:absolute;left:8px;top:8px;width:8px;border-top:1px dotted #ece;}.layui-treeSelect .ztree li span.button.ico_open{display:inline-block;position:relative;top:1px;}.layui-treeSelect .ztree li span.button.ico_close{display:inline-block;position:relative;top:1px;}.layui-treeSelect .ztree li span.button.ico_open:before{content:"\\e643";}.layui-treeSelect .ztree li span.button.ico_close:before{content:"\\e63f";}';
                var $head = $('head');
                var ztreeStyle = $head.find('style[ztree]');

                if (ztreeStyle.length === 0) {
                    $head.append($('<style ztree>').append(ext))
                }
                return a;
            },
            event: function (evt, el, fn) {
                $('body').on(evt, el, fn);
            }
        };

        a.init();
        return new TreeSelect();
    };

    /**
     * 重新加载trerSelect
     * @param filter
     */
    TreeSelect.prototype.refresh = function (filter) {

    };

    /**
     * 选中节点，因为tree是异步加载，所以必须在success回调中调用checkNode函数，否则无法获取生成的DOM元素
     * @param filter lay-filter属性
     * @param id 选中的id
     */
    TreeSelect.prototype.checkNode = function (filter, id) {

    };

    /**
     * 撤销选中的节点
     * @param filter lay-filter属性
     * @param fn 回调函数
     */
    TreeSelect.prototype.revokeNode = function (filter, fn) {

    }

    //输出接口
    var mod = new TreeSelect();
    exports(MOD_NAME, mod);
});    