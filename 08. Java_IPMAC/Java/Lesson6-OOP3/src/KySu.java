public class KySu extends CanBo {
    private String nganhDaoTao;

    public void setNganhDaoTao(String _nganhDaoTao) {
        this.nganhDaoTao = _nganhDaoTao;
    }

    public String getNganhDaoTao() {
        return this.nganhDaoTao;
    }

    @Override
    public void inCanBo() {
        super.inCanBo();
        System.out.println("Nganh dao tao: " + this.nganhDaoTao);
    }
}
