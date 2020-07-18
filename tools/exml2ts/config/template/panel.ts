module game
{
	export class [panelName]Data extends DataBase
	{
        public Destroy()
		{
			super.Destroy();
		}
	}

	export class [panelName] extends UIComponentBase
	{
[property]

		public info:[panelName]Data;
		public constructor()
		{
			super("[panelName]Skin", true);
		}

		public InitData(data:[panelName]Data)
		{
			if(data == null)
				return;
			this.info = data;

[event]
		}

		public Destroy()
		{
			if(this.info != null)
				this.info.Destroy();
		}
	}
}