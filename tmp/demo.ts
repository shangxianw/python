module game 
{
    export class AAAC extends UICtrlBase
    {
        public constructor()
        {
            super();
        }

        ////////////////////////////////////////////////////////////////////////////////////////////////
        //声明界面要引用的资源组 一定要有 公共资源不需要引用
        protected GetResGroup():string[]
        {
             return [];
        }
        //声明父窗口 可以没有 默认是panelLayer
        protected GetParent():any
        {
            return GameLayerManager.gameLayer().panelLayer;
        }
        //声明要实例化的EXML类 一定要有!!!
        protected GetPanelClass():any
        {
            return AAA;
        }
        /////////////////////////////////////////////////////////////////////////////////////////////////////

        public OnMessage(itype:number, data:any): void
        {
            super.OnMessage(itype, data);
            if(itype == PanelMessageType.OnShow)
            {
                this.ShowUI(false, 0, 0, 0, false, true, data);
            }
            else if(itype == PanelMessageType.OnHide)
            {
                this.ClosePanel(4);
            }
            else if(itype == PanelMessageType.OnDestroy)
            {
                this.DestroyPanel();
            }
        }

        protected Destroy()
        {

        }
    }
}