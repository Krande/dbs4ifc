// hello_project.cs, this software use IfcSharp (see https://github.com/IfcSharp)

using ifc;

class hello_project
{
    static void Main(string[] args)
    {
        //#####################################################################
        try
        {
            ifc.Repository.CurrentModel = new ifc.Model(Name: "hello_project_output");

#if IFC2X3
new ifc.Project(_OwnerHistory:null,RepresentationContexts:null,UnitsInContext:null,GlobalId:ifc.GloballyUniqueId.NewId(),Name:new ifc.Label("my first ifc-project"));  // appends entity to ifc.Repository.CurrentModel
#else
            new ifc.Project(GlobalId: ifc.GloballyUniqueId.NewId(),
                Name: new ifc.Label("my first ifc-project")); // appends entity to ifc.Repository.CurrentModel
#endif

            ifc.Repository.CurrentModel.ToStepFile(); // creates hello_project_output.ifc (step-format)
            ifc.Repository.CurrentModel
                .ToHtmlFile(); // creates hello_project_output.html in step-format with syntax highlighting
            ifc.Repository.CurrentModel.ToSqliteFile();// creates hello_project_output.sqlite3 with the default option exportCompleteSchema=false 
        }
        catch (System.Exception e)
        {
            System.Console.WriteLine(e.Message);
        }
    }
} //########################################################################################################################