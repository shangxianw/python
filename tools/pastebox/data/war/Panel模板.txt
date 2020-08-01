module home
{
	export class DemoPanelData extends ViewData
	{
		protected init()
		{

		}
		
		protected destroy()
		{
			
		}

		public packData()
		{

		}
	}

	export class DemoPanel extends ViewBase
	{
		public info:DemoPanelData;
		public initData(data:any=null)
		{
			this.info.packData();
		}

		protected destroy()
		{

		}

		public open()
		{

		}
	}
}