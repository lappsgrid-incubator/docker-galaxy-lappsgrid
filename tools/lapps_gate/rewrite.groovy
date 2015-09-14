import groovy.xml.*

def parser = new XmlParser()
File directory = new File('.')
directory.eachFileMatch(~/.*\.xml$/) { File file ->
	def tool = parser.parse(file)
	String service = tool.command.text().split()[1]
	tool.command[0].value = "invoke.lsd $service \$input \$username \$password \$output"
	tool.inputs[0].appendNode 'param', [name:'username', type:'text', value:'tester', label:'Username']
	tool.inputs[0].appendNode 'param' , [name:'password', type:'text', value:'tester', label:'Password']
	
	def writer = new PrintWriter(new FileWriter(file))
	def printer = new XmlNodePrinter(writer, "\t")
	printer.print(tool)
	println "Wrote ${file.path}"
}
