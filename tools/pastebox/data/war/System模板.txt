module war
{
	export class DemoSystem extends SystemBase
	{
		protected init()
		{
			this.sysType = System.Demo;
		}

		protected destroy()
		{

		}
		
		public update(entity:EntityBase, deltaTime:number)
		{
			if(entity == null)
				return;
			
			let posCom = entity.getComponent(Component.Pos) as PosCom;
			if(posCom == null)
				return;
		}
	}
}