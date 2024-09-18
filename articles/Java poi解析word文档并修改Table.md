# Java poi解析word文档并修改Table

实际背景：解析swagger导出的api.json文件，加载以docx结尾的word模板，并将处理好的数据填写进去

# 一、必要的基础概念

## 1、关于word

1. word采用的是**XML**文件格式。在.docx文件中，文档的内容被存储为一系列的XML文件，这些文件通过ZIP压缩打包在一起。另外具体的word支持的文件格式可参考：https://learn.microsoft.com/zh-cn/office/compatibility/office-file-format-reference

2. 除了body等结构标签，这里只列举一些基于xwpf解析的，对于开发特别重要的标签：

   1. `<w:p w14:paraId="096D82C2">`：这是一个**段落(Paragraph)元素标签**，**段落是word中最基础的也是最重要的使用标签**。其中`w14:paraId` 属性是特定于Microsoft Word 2010的，用于唯一标识段落。p标签下通常包含：

      1. `<w:r> `：这是段落中的文本元素的标签，通常包含文本的样式`<w:rPr>`以及文本本身`<w:t>`，因此这个标签的作用主要是为了正确地处理段落中不同文本中的字符编码和格式。
      2. `<w:t>`：真正放置文本的标签，只包含文本具体内容。一个`<w:p>`段落可以有多个`<w:r> `标签，一个`<w:r> `只包含一个`<w:t> `标签。

   2. `<w:tcPr>`：表格单元格属性标签，包含了定义单元格样式的各种属性。**只要标签带`Pr`的都是属性标签，例如`<w:rPr>`、`<w:pPr>`、`<w:tblPr>`等**。常见的属性有：

      1. `<w:tcW w:w="687" w:type="dxa"/>`：定义了单元格的宽度，其中`w:w`属性值“687”和`w:type`属性值“dxa”一起表示单元格的宽度为687个“dxa”单位（“dxa”是Word中用于度量的单位，1“dxa”等于1/1440英寸）。
      2. `<w:gridSpan w:val="2"/>`：表示该单元格的左右合并行为，即单元格跨越的列数，`w:val`属性值为“2”意味着这个单元格将跨越2列。
      3. `<w:vMerge w:val="continue"/>`：表示该单元格的垂直合并行为，` w:val="continue"`属性值为"continue"则表示这个单元格是一个被合并了的单元格，并希望下一行的某些单元格与上一行合并的单元格继续垂直合并。若属性值为"restart"则表示这个单元格为开始合并单元格，即在这一个单元格开始形成一个新的垂直合并序列。
      4. `<w:vAlign w:val="center"/>`：定义了单元格中内容的垂直对齐方式，`w:val`属性值“center”表示内容居中对齐。

   3. `<w:tbl>`：表格标签。通常包含以下标签：

      1. `<w:tblGrid>`：表格的网格标签，包含`<w:gridCol w:w="1330"/>`表中的列标签，`w:w="1330"`代表每列的宽度，默认使用dxa为单位指定宽度。每当我们增加列的时候就会从网格标签入手。
      2. `<w:tr>`: 表格的行标签。一个`<w:tr>`行标签包含多个`<w:tc>`单元格标签，在不考虑合并单元格的情况下，有多少个单元格也就表示有多少个`<w:gridSpan/>`列。
      3. `<w:tc>`: 表格的单元格标签。里面通常会有`<w:p>`来包含单元格的内容，结构就又回到上面讲的段落标签。一个`<w:tc>`单元格可以有多个`<w:p>`段落。

   4. `<w:pict>`：图片元素标签，被包含在`<w:p>`段落中的`<w:r> `标签下，同样地一个`<w:p>`段落可以有多个`<w:r> `标签，一个`<w:r> `只包含一个`<w:pict> `标签。在标准的Open XML中，图片通常通过`<w:drawing>`元素内的`<a:graphic>`（属于DrawingML命名空间）来表示。其下包含的标签：

      1. `<v:shape id="_x0000_i1025" o:spt="75" alt="1O2A0269" type="#_x0000_t75" style="height:232.6pt;width:413.55pt;" filled="f" o:preferrelative="t" stroked="f" coordsize="21600,21600">`：定义了一个矢量形状，可以指定图片的各种特性，包含下面2-8的标签。

         - ‌`o:spt="75"`‌：这个属性是Office特有的，`o:`命名空间通常用于Office特定的属性和元素。`spt`可能代表“shape type”（形状类型），而`75`是该形状类型的编号。不同的编号对应不同的预定义形状，如矩形、圆形、箭头等。
         - ‌`alt="1O2A0269"`‌：`alt`属性通常用于提供图片的替代文本，以便在图片无法显示时（如屏幕阅读器读取文档时）提供信息。但在这里，它可能只是用作某种标识符或元数据，而不是实际的替代文本。

      2. ` <v:path/>` ：通常用于描述形状轮廓，但在这个上下文中，由于图片没有轮廓，所以路径是空的。

      3. ` <v:fill on="f" focussize="0,0"/>` ：表明形状不被填充，且没有聚焦大小。

      4. `<v:stroke on="f"/>`：确认形状没有描边。

      5. ` <v:imagedata r:id="rId5" o:title="1O2A0269"/>` ：这是图片数据的实际引用，`rId5`是关系ID，指向文档的图像部分，`o:title`可能用于存储图片标题或标识符。

      6. ` <o:lock v:ext="edit" aspectratio="t"/>` ：锁定图片的宽高比，防止手动调整时失真。

      7. ` <w10:wrap type="none"/>` ：表明图片没有文字环绕。

      8. `<w10:anchorlock/>`：锁定图片的位置，防止随意移动。

         

## 2、关于poi-xwpf重要的类及api

1. **XWPFDocument**: Word文档整体，它**包含所有的文档信息**包括页眉页脚和文档中的所有内容。重要的属性解释：
   1. `bodyElements`：List，按顺序包含body中的所有元素，基本以一个段落为一个对象、一个table一个对象。
   2. `paragraphs`：List，按顺序包含所有的段落信息，对应`<w:p>`标签。
   3. `tables`：List，按顺序包含所有的表格信息，对应`<w:tbl>`标签。
   4. `ctDocument`：CTDocument1，包含word文档所有的xml。通过`ctDocument`属性，开发者可以访问和修改Word文档的底层XML结构，这对于需要进行复杂操作或需要直接与OOXML规范交互的场景非常有用。

2. **XWPFParagraph**: 段落，对应`<w:p>`标签。值得说明的是，类中包含XWPFDocument document这个属性，意味着xwpf在处理时，会将document都完整地复制到所有的段落对象中以便取用。
3. **XWPFTable**: 表格，对应`<w:tbl>`标签。`CTTbl`代表`CTable`，它是WordprocessingML（Word文档的XML格式）中用于定义表格的底层类。通过使用`CTTbl`类，开发者可以在Java代码中创建、修改和操作Word文档中的表格结构。
4. **XWPFTableRow**：行，对应`<w:tr>`标签。可以通过使用`CTRow`对象来设置表格行的属性。另外类中同样包含完整的table对象。
5. **XWPFTableCell**: 单元格，对应`<w:tc>`标签。可以通过设置`CTTc`对象来设置单元格的属性。包含完整的row对象。类中的`List<XWPFTable> tables`属性用于存储或管理与当前单元格相关的表格集合。在Word文档的XML结构中，一个单元格可能包含嵌套的表格（例如，合并单元格中的子表格）。因此，`tables`属性可能是用于处理这种复杂表格结构的，允许开发者访问和操作单元格内的所有子表格。
6. **XWPFRun**: 运行对象，对应`<w:r>`标签，**是段落中最基本的文本处理单位**。内部同样是操作CTR和CTText，但是已经不用再关心它们是什么结构了，因为通过run已经可以直接处理单元格中的文本内容。

# 二、具体操作

## 1、pom.xml引入依赖

```xm
<dependency>
    <groupId>org.apache.poi</groupId>
    <artifactId>poi</artifactId>
    <version>5.2.3</version>
</dependency>
<dependency>
    <groupId>org.apache.poi</groupId>
    <artifactId>poi-ooxml</artifactId>
    <version>5.2.3</version>
</dependency>
```

## 2、读取json文档并处理

### 方法1:**java.io.FileInputStream**

```java
// 读取json文件内容
FileInputStream jsonFis = new FileInputStream(new File("/path/to/api.json"));
BufferedReader bufferedReader = new BufferedReader(new InputStreamReader(jsonFis));
String line;
StringBuilder jsonContent = new StringBuilder();
while ((line = bufferedReader.readLine()) != null) {
    jsonContent.append(line);
}

// 使用Fastjson解析JSON字符串
JSONObject jsonObject = JSON.parseObject(jsonContent.toString());
```

### 方法2：**org.springframework.util.ResourceUtils**

```java
FileInputStream jsonFis = new FileInputStream(ResourceUtils.getFile("classpath:api.json"));
BufferedReader bufferedReader = new BufferedReader(new InputStreamReader(jsonFis));
```

### 方法3：**org.springframework.core.io.ClassPathResource**

```java
ClassPathResource classPathResource = new ClassPathResource("api.json");
InputStreamReader inputStreamReader = new InputStreamReader(classPathResource.getInputStream());
```

## 3、读取word文档

使用上面读取json文件的同样方法得到FileInputStream wordFis，然后使用以下代码：

```java
XWPFDocument doc = new XWPFDocument(wordFis);
```

为了方便理解，我将模板中的表格截图放在下面：

![image-20240914152644978](/Users/fengse/Library/Application Support/typora-user-images/image-20240914152644978.png)



## 4、填写数据

```java
// 循环得到word表格
for (XWPFTable table:doc.getTables()){
  // 因为需要对表格进行操作，往往需要索引，所以推荐使用fori
  for (int rowIndex = 0; rowIndex < row.getRows().size(); rowIndex++) {
  	XWPFTableRow row = table.getRow(rowIndex);
    for (int cellIndex = 0; cellIndex < row.getTableCells().size(); cellIndex++) {
    	XWPFTableCell cell = row.getCell(cellIndex);
      String text = cell.getText(); // 获取单元格的所有文本内容
      // 追加和替换文本
			if (text.contains("□")) {
        // 只会将新给出的text追加在旧的text后面，不会替换
				cell.setText("☑");
        // 如果需要替换文本，推荐下面这种写法，操作p中的r
        cell.getParagraphs().forEach(p -> p.getRuns().forEach(run -> {
        	if (run.getText(0).contains("□")) {
          	run.setText("☑", 0);
          }
        }));
			}
	    //  操作表格，字段列举所在单元格是垂直合并了两行的单元格
  		if (text.contains("字段列举")) {
        int rawSize = 5; // 根据需要加入的数据大小计算出行数，这里假设为5行
        int rowPos = rowIndex;// 当前操作行位置
        int cellPos = cellIndex + 1; // 当前操作单元格初始位置为获取文本数据的向右一格
        for (int i = 0; i < rawSize; i++) {
          // 如果i为0、1行，则将数据填入
          if (i < 2) {
            row = table.getRow(rowPos);
          } eles { // 否则新建行
            row = table.insertNewTableRow(rowPos);
            row.setHeight(row.getHeight());
            // 新建前面需要的合并单元格：前面有3个空白单元格需要创建并合并
            for (int j = 0; j < 3; j++) {
            	XWPFTableCell newTableCell = row.addNewTableCell();
              // 由于前面已经有了合并单元格，所以这里只需要设置单元格属性为 continue
              newTableCell.getCTTc().addNewTcPr().addNewVMerge().setVal(STMerge.CONTINUE);
            }
          }
          // 需要填入6列的数据
        	for (int j = 0; j < 6; j++) {
            XWPFTableCell rowCell = row.getCell(cellPos + j);
            if(rowCell == null){
              rowCell = row.addNewTableCell();
            }
            // 通过观察得到原本行中第3个单元格存在左右合并单元格
            if(i>=2 && j==2){
              // 获取CTTc对象
        			CTTc ctTc = rowCell.getCTTc();
							// 创建CTTcPr对象，如果已经存在则获取
        			CTTcPr ctTcPr = ctTc.getTcPr() == null ? ctTc.addNewTcPr() : ctTc.getTcPr();
							// 设置跨列属性，值为2表示单元格将横跨两列
        			CTDecimalNumber gridSpanNumber = ctTcPr.addNewGridSpan();
        			gridSpanNumber.setVal(BigInteger.valueOf(2));
            }
            // 根据自己需要的算法计算单元格该填入的内容
            if (j % 2 == 0) {
              rowCell.setText(String.valueOf(i * 3 + j / 2 + 1));
            } else {
              rowCell.setText("内容"+ (i * 3 + (j - 1) / 2));
            }
          }
          rowPos++；
        }
      }
    }
  }
}
```

## 5、导出word文档

```java
wordFis.close();
FileOutputStream out = new FileOutputStream("/path/to/output/file" + (docNum++) + ".docx"); // 在处理文档的循环外自行增加一个标识，如docNum文件数
doc.write(out);
doc.close();
out.close();
```

# 三、更多优秀文档

## 1、[【使用分享】一文掌握WordXML，OOXML规范](https://blog.csdn.net/qq_43248802/article/details/130685143)

## 2、[Java操作Word文档](https://blog.csdn.net/Zyw907155124/article/details/139991278)



# 感谢阅读，欢迎在评论区留下你的想法！
