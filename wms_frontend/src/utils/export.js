// 导出工具函数，使用 xlsx 库将数据导出为 Excel 文件
import * as XLSX from 'xlsx'

export function exportToExcel({ data, header, filename = '库存数据.xlsx' }) {
  // 组装表头和数据
  const wsData = [header]
  data.forEach(item => {
    wsData.push(header.map(key => item[key] ?? ''))
  })
  const ws = XLSX.utils.aoa_to_sheet(wsData)
  const wb = XLSX.utils.book_new()
  XLSX.utils.book_append_sheet(wb, ws, 'Sheet1')
  XLSX.writeFile(wb, filename)
}
