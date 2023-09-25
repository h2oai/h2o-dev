package water.parser.parquet;

import water.H2O;
import water.fvec.Frame;
import water.parser.BinaryFormatExporter;
import water.util.ExportFileFormat;

public class ParquetExporter implements BinaryFormatExporter {

    @Override
    public H2O.H2OCountedCompleter export(Frame frame, String path, boolean force, String compression, boolean writeChecksum) {
        return new ExportParquetDriver(frame, path, force, compression, writeChecksum);
    }

    @Override
    public boolean supports(ExportFileFormat format) {
        return ExportFileFormat.parquet.equals(format);
    }

    private class ExportParquetDriver extends H2O.H2OCountedCompleter<ExportParquetDriver> {

        Frame _frame;
        String _path;
        boolean _force;
        String _compression;
        boolean _writeChecksum;

        public ExportParquetDriver(Frame frame, String path, boolean force, String compression, boolean writeChecksum) {
            _frame = frame;
            _path = path;
            _force = force;
            _compression = compression;
            _writeChecksum = writeChecksum;
        }

        @Override
        public void compute2() {
            // multipart export
            FrameParquetExporter parquetExporter = new FrameParquetExporter();
            parquetExporter.export(this, _path, _frame, _force, _compression, _writeChecksum);
        }
    }
}
